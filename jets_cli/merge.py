import os, sys, util
from PyPDF2 import PdfFileReader, PdfFileWriter

path = os.path.realpath(__file__)
path = path.replace("merge.py","")
merge_path = path + "Articles/Merged/"
all_path = path + "Articles/All/"


def merge(vol_num, issue_num):
    folder = "Vol " + vol_num +"/"
    if issue_num == "0":
        issues = []
        for file in os.listdir(path):
            if file.startswith(vol_num + "."):
                num = util.get_nums(file)[0]
                issues.append(num)
        for issue_num in issues:
            merge_issues(folder, vol_num, issue_num)
        merge_vol(vol_num)
    else:
        merge_issues(folder, vol_num, issue_num)

def merge_issues(folder, vol_num, issue_num):
    merged_path = merge_path + folder
    if not os.path.exists(merged_path):
        os.mkdir(merged_path)
    output = merged_path + "Issue " + str(issue_num) + ".pdf"
    file_out = open(output, 'ab')
    writer = PdfFileWriter()
    for article in os.listdir(path):
        if article.startswith(vol_num + "." + issue_num):
            file = open(all_path + article, 'rb')
            pdf = PdfFileReader(file)
            for page in range(pdf.getNumPages()):
                writer.addPage(pdf.getPage(page))
            writer.write(file_out)
            file.close()
    file_out.close()

def merge_vol(vol_num):
    for folder in os.listdir(merge_path):
        if folder == "Vol " + vol_num:
            output = merge_path + folder + "/Vol " + vol_num + ".pdf"
            file_out = open(output, 'ab')
            writer = PdfFileWriter()
            for file in os.listdir(merge_path + folder):
                pdf_file = open(merge_path + folder + "/" + file, 'rb')
                pdf = PdfFileReader(pdf_file)
                for page in range(pdf.getNumPages()):
                    writer.addPage(pdf.getPage(page))
                writer.write(file_out)
                pdf_file.close()
            file_out.close()
