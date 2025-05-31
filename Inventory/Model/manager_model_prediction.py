import spacy

# Load the saved model
nlp = spacy.load("inventory_manager_nlu_model")

# Example test texts
test_texts = [
    # add_item
    "Add 10 apples to the stock.",
    "Please insert 3 new laptops.",
    "I want to include 5 chairs in the inventory.",
    "Can you put 7 bottles of water into storage?",
    "Increase the quantity of notebooks by 12.",
    "Restock 20 pens in the warehouse.",
    "Add some more keyboards to the list.",
    "Please top up the shelves with 8 boxes of cereal.",
    "Add a batch of 15 monitors.",
    "Insert 10 cartons of juice.",
    "Put 6 packs of batteries on the inventory.",
    "I need to add 4 new smartphones.",
    "Top up the stock with 9 bags of rice.",
    "Add more items: 14 t-shirts.",
    "Update the inventory by adding 11 chairs.",
    "Can you replenish 13 bottles of soda?",
    "Add 2 tables to the warehouse.",
    "Please increase stock by 7 headphones.",
    "I want to insert 10 new books.",
    "Add 5 packs of printer paper.",
    "Put 3 new printers into inventory.",
    "Include 6 bags of flour.",
    "Add some extra chairs to the storage.",
    "Increase stock by 8 bottles of shampoo.",
    "Insert 9 new USB drives.",

    # delete_item
    "Remove 5 old chairs from inventory.",
    "Delete 3 broken laptops.",
    "Please erase 4 outdated monitors.",
    "Take away 7 empty boxes.",
    "Remove 10 packs of expired batteries.",
    "Can you discard 6 damaged printers?",
    "Delete 8 obsolete phones.",
    "Remove some items: 12 chairs.",
    "Remove 9 cartons of spoiled juice.",
    "Clear 5 bags of stale flour.",
    "Delete 4 outdated smartphones.",
    "Remove 3 worn-out keyboards.",
    "Please get rid of 6 damaged books.",
    "Delete 7 old headphones from stock.",
    "Remove 2 tables that are no longer used.",
    "Take out 10 bottles of expired soda.",
    "Remove 8 defective printer cartridges.",
    "Delete 4 broken USB drives.",
    "Remove 11 bottles of old shampoo.",
    "Erase 3 outdated bags of rice.",
    "Remove 7 damaged boxes of cereal.",
    "Delete 5 expired packs of paper.",
    "Take away 6 old monitors.",
    "Remove 4 broken chairs.",
    "Discard 10 empty water bottles.",

    # check_quantity
    "How many chairs do we have left?",
    "Check the stock for laptops.",
    "What’s the quantity of monitors in inventory?",
    "Tell me how many bottles of water are available.",
    "Do we have enough pens in stock?",
    "How many keyboards are currently stored?",
    "Check the number of t-shirts in the warehouse.",
    "What’s the count of printer cartridges?",
    "Show me the quantity of smartphones.",
    "How many bags of flour are left?",
    "Check how much rice we have.",
    "What’s the inventory count for headphones?",
    "How many packs of batteries are available?",
    "Show me the quantity of books in stock.",
    "What is the current stock of cereal boxes?",
    "Tell me the amount of expired juice cartons.",
    "How many printer papers are left?",
    "Check the stock of USB drives.",
    "How many bottles of shampoo do we have?",
    "Tell me the number of monitors available.",
    "How many tables are currently in inventory?",
    "Show the count of old chairs.",
    "Check quantity of broken laptops.",
    "How many empty boxes remain?",
    "What’s the number of damaged books?",

    # show_inventory
    "Show me all the items in stock.",
    "Display the current inventory.",
    "List all products available.",
    "What is in the warehouse right now?",
    "Show the complete stock list.",
    "Give me an overview of the inventory.",
    "Display all items stored.",
    "List the goods currently available.",
    "Show me the items we have.",
    "What’s currently in the storage?",
    "Display the warehouse contents.",
    "Show the full list of inventory items.",
    "Give me the inventory details.",
    "Show me all products in stock.",
    "List all items present in the warehouse.",
    "Show the stock availability.",
    "Display items currently in inventory.",
    "Give me a summary of goods in stock.",
    "Show what we have stored.",
    "List the inventory right now.",
    "Show the warehouse inventory report.",
    "Display the full stock status.",
    "Give me the current products list.",
    "Show all inventory items available.",
    "List what’s in the stock now."
]

# Predict label for each test text
for text in test_texts:
    doc = nlp(text)
    cats = doc.cats
    # Get the predicted label with highest score
    predicted_label = max(cats, key=cats.get)
    confidence = cats[predicted_label]
    print(f"Text: '{text}'")
    print(f"Predicted label: {predicted_label} (confidence: {confidence:.3f})\n")
