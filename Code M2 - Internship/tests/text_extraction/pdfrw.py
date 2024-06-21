from pdfrw import PdfReader

reader = PdfReader('/home/cristel/PycharmProjects/M2 Internship/Download_papers/PMC9389945.pdf')
print(reader.Info.Title)
print(reader.Info.Author)


