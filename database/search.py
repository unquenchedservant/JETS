from database import executor

def author_table(author_name):
    """
    Search the author table for a specific author

    Parameters:
    author_name (string): the author name to search

    Returns:
    True  : the author was found, item in table
    False : author was not found, item not in table
    """
    sql = "SELECT * FROM authors WHERE author_name = '{}'".format(author_name)
    data = executor.select(sql)
    if len(data) == 0:
        return False
    else:
        return True

def articles_table(full_number):
    """
    Search the articles table for a specific article

    Parameters:
    full_number (string): if the full_number is in the table, gets information

    Returns:
    True  : the article number was found, item in table
    False : article number was not found, item not in table
    """
    sql = "SELECT * FROM articles WHERE full_number = '{}'".format(full_number)
    data = executor.select(sql)
    if len(data) == 0:
        return False
    else:
        return True
