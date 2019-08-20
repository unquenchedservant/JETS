import os, click, sys, database
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile
import sqlite3

path = os.path.realpath(__file__)
path = path.replace("util.py","")
path = path + "Articles/"
all_path = path + "All/"
merge_path = path + "Merged/"
author_path = path + "Authors/"

def start():
    if not os.path.exists(path + "author.db"):
        database.create_database()
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(all_path):
        os.mkdir(all_path)
    if not os.path.exists(merge_path):
        os.mkdir(merge_path)

def string_strip(string):
    if string.endswith(" ") or string.endswith("."):
        string = string[:-1]
        return string_strip(string)
    else:
        string = string.strip()
        return string

def p(msg):
    click.echo()
    click.echo(msg)

def check_vol(vol):
    if not vol.isdigit():
        p("Please enter an integer for volume")
        sys.exit()
    vol = int(vol)
    if not vol >= 0 and vol <= 62:
        p("Please enter 1-62 for Volume")
        sys.exit()


def check_issue(issue):
    if not issue.isdigit():
        p("Please eneter an integer for issue")
        sys.exit()
    issue = int(issue)
    if not issue >= 0 and issue <= 4:
        p("Please enter 1-4 for Issue")
        sys.exit()


def get_info(pdf):
    f = open(pdf, 'rb') #open the right article as "f"
    pdf = PdfFileReader(f)
    info = pdf.getDocumentInfo() #gets metadata
    f.close()
    info = [info.title, info.author]
    return info

def get_num(vNum, iNum, aNum):
    vNum = check_digit(vNum)
    iNum = check_digit(iNum)
    aNum = check_digit(aNum)
    num = vNum + "." + iNum + "." + aNum
    return num

def write_info(pPath, name, author):
    f = open(pPath, 'rb')
    pdf = PdfFileReader(f)
    writer = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        writer.addPage(pdf.getPage(page))
    writer.addMetadata({
        '/Author': author,
        '/Title': name
    })
    fout = open(path + 'tem.pdf', 'ab')
    writer.write(fout)
    fout.close()
    f.close()
    copyfile(path + "tem.pdf", pPath)
    os.remove(path + "tem.pdf")

def check_digit(num):
    if len(str(num)) == 1:
        num = "0" + str(num)
    return num

def get_possible_names(name):
    found_names = []
    click.echo()
    name_split = name.split(" ")
    full_name_list = database.get_names()
    for x in name_split:
        for author in full_name_list:
            print(author)
            names = author.lower()
            if name.lower() == names:
                return None
            if x.lower() in names and len(x) > 2:
                if not author in found_names:
                    found_names.append(author)
    if len(found_names) > 0:
        click.echo("Found Possibilities: "  + str(len(found_names)))
        click.echo()
        for x, author in enumerate(found_names):
            click.echo(str(x + 1) + " - " + author)
        click.echo(str(x + 2) + " - New Author")
        click.echo()
        value = click.prompt("Option", type = click.IntRange(1, len(found_names)+1))
        if int(value) == x+2:
            return None
        else:
            name = found_names[value -1]
            return name

def get_numbers(term, canAppend=True):
    cDot = term.count(".")
    vol_num = issue_num = article_num = "0"
    if cDot >= 0:
        vol_num = term.split(".")[0]
        check_vol(vol_num)
    if cDot >= 1:
        issue_num = term.split(".")[1]
        check_issue(issue_num)
    if cDot == 2:
        article_num = term.split(".")[2]
    if not article_num.isdigit():
        p("Please enter an integer for article")
        sys.exit()
    if canAppend == 1:
        vol_num = check_digit(vol_num)
        issue_num = check_digit(issue_num)
        article_num = check_digit(article_num)
    return (vol_num, issue_num, article_num)

def get_nums(article):
    number = article.split(" - ")[0]
    numbers = number.split(".")
    volume_number, issue_number, article_number = [numbers[0], numbers[1], numbers[2]] 
    return [number, volume_number, issue_number, article_number]

def get_title(article):
    title = article.split(" - ", 1)[1]
    title = title.split(".pdf")[0]
