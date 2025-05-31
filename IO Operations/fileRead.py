# file_name = "D:\\Git cmd.rtf"
file_name = "D:\\Youtube"
try:
    print(open(file_name, 'rt').read())
except FileNotFoundError:
    print('File Not Found. Please Check the File or Path.')
except Exception as e:
    print('unhandled Exception')
    print(e)
