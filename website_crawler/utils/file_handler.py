from os import makedirs, path  # imports from the python os module to be able to create directories and file paths

crawler_files_dir = "crawler_files/"
data_file_paths = ("/queue.txt", "/crawled.txt", "/webpage_")


# each website domain you crawl is a separate folder/directory containing crawler (data) files
def create_website_dir(directory):
    if not path.exists(crawler_files_dir + directory):
        print("Creating crawler directory: %s" % directory)
        makedirs(crawler_files_dir + directory)


# create queue and crawled files (if not created) and add the start url to queue
def create_data_files(domain_name, base_url):
    queue = crawler_files_dir + domain_name + data_file_paths[0]
    crawled = crawler_files_dir + domain_name + data_file_paths[1]
    """
    # create crawler files if files not already exists
    if not path.isfile(queue):
        write_file(queue, base_url)
    if not path.isfile(crawled):
        write_file(crawled, '')
    """
    write_file(queue, base_url)
    write_file(crawled, base_url)


def create_html_files(domain_name, depth_id, html):
    html_file_path = crawler_files_dir + domain_name + data_file_paths[2] + str(depth_id) + ".html"
    # print("Creating html file: %s" % html_file_path)
    write_file(html_file_path, html)
    print("Downloading webpage to <%s>" % html_file_path)


# creates a new file
def write_file(file_path, data):
    file = open(file_path, 'w', encoding="utf-8")
    file.write(data)
    file.close()


# add data onto an existing file
def append_to_file(file_path, data):
    with open(file_path, 'a') as file:
        file.write(data + "\n")


# delete the contents of a file
def delete_file_contents(file_path):
    with open(file_path, 'w'):
        pass


# read a file and convert each line to set items
def file_to_set(file_path):
    results = set()  # create empty set
    with open(file_path, 'rt') as file:
        for line in file:
            results.add(line.replace('\n', ""))  # adds each line to set excluding newline character
    return results


# iterate through a set, each item will be a new line in the file
def set_to_file(links, file_path):
    delete_file_contents(file_path)
    for link in sorted(links):
        append_to_file(file_path, link)


def get_queue_file_path(dir_name):
    return crawler_files_dir + dir_name + data_file_paths[0]


def get_crawled_file_path(dir_name):
    return crawler_files_dir + dir_name + data_file_paths[1]
