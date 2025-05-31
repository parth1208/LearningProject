import random
import warnings  # <-- Add this line

import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from spacy.training.example import Example
from spacy.util import minibatch, compounding

# Suppress specific spaCy warnings
warnings.filterwarnings("ignore", category=UserWarning, module='spacy.pipeline.attributeruler')
warnings.filterwarnings("ignore", category=UserWarning, module='spacy.pipeline.lemmatizer')

# Load data
df = pd.read_csv(r"D:\Learning Project\Inventory\Model\Traing_Data\inventory_training_data.csv")
unique_labels = df["label"].unique().tolist()

# Split data
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])

# Load pretrained medium English model
# nlp = spacy.load("en_core_web_md")  --new model
nlp = spacy.load("inventory_manager_nlu_model")

# Proper config for adding textcat with exclusive_classes
textcat_config = {
    "model": {  # exclusive_classes should be inside the model block
        "@architectures": "spacy.TextCatCNN.v2",
        "exclusive_classes": True,  # Moved here
        "tok2vec": {
            "@architectures": "spacy.Tok2Vec.v2",
            "embed": {
                "@architectures": "spacy.MultiHashEmbed.v2",
                "width": 96,
                "rows": [5000, 2500, 1000, 1000, 1000],
                "attrs": ["ORTH", "LOWER", "PREFIX", "SUFFIX", "SHAPE"],
                "include_static_vectors": False,
            },
            "encode": {
                "@architectures": "spacy.MaxoutWindowEncoder.v2",
                "width": 96,
                "window_size": 1,
                "maxout_pieces": 3,
                "depth": 2,
            },
        },
    },
}

if "textcat" not in nlp.pipe_names:
    textcat = nlp.add_pipe("textcat", config=textcat_config, last=True)
else:
    textcat = nlp.get_pipe("textcat")

# Add missing labels only once
for label in unique_labels:
    if label not in textcat.labels:
        textcat.add_label(label)


# Prepare training examples function
def make_examples(nlp, df, unique_labels):
    examples = []
    for _, row in df.iterrows():
        doc = nlp.make_doc(row["text"])
        cats = {label: float(label == row["label"]) for label in unique_labels}
        examples.append(Example.from_dict(doc, {"cats": cats}))
    return examples


train_examples = make_examples(nlp, train_df, unique_labels)
val_examples = make_examples(nlp, val_df, unique_labels)

# Initialize optimizer - important to call initialize AFTER adding labels and before training
nlp.initialize(lambda: train_examples)

optimizer = nlp.optimizer if hasattr(nlp, "optimizer") else nlp.resume_training()

n_iter = 20
batch_sizes = compounding(4.0, 32.0, 1.5)

for epoch in range(n_iter):
    random.shuffle(train_examples)
    losses = {}

    batches = minibatch(train_examples, size=batch_sizes)
    for batch in batches:
        nlp.update(batch, sgd=optimizer, losses=losses, drop=0.3)

    # Validation accuracy calculation
    correct = 0
    total = 0
    for example in val_examples:
        pred_doc = nlp(example.text)
        pred_label = max(pred_doc.cats, key=pred_doc.cats.get)
        true_label = max(example.reference.cats, key=example.reference.cats.get)
        if pred_label == true_label:
            correct += 1
        total += 1
    val_accuracy = correct / total

    print(f"Epoch {epoch + 1}, Loss: {losses.get('textcat', 0):.4f}, Val Accuracy: {val_accuracy:.3f}")

# Save model
nlp.to_disk("inventory_manager_nlu_model")
print("Model saved to 'inventory_manager_nlu_model'")

# Final evaluation on validation set
correct = 0
total = 0
for example in val_examples:
    pred = nlp(example.text)
    pred_label = max(pred.cats, key=pred.cats.get)
    true_label = max(example.reference.cats, key=example.reference.cats.get)
    if pred_label == true_label:
        correct += 1
    total += 1
accuracy = correct / total
print(f"Final Validation Accuracy: {accuracy:.3f}")

print(df['label'].value_counts())
