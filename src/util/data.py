import os

def get_20_pdf(data_path='data'):
    for role in os.listdir(data_path):
        role_path = os.path.join(data_path, role)
        if not os.path.isdir(role_path):
            continue

        pdf_files = [f for f in os.listdir(role_path) if f.lower().endswith('.pdf')]
        pdf_files.sort() 

        delete = pdf_files[20:]

        for file in delete:
            file_path = os.path.join(role_path, file)
            os.remove(file_path)

if __name__ == '__main__':
    get_20_pdf()