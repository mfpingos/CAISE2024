# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:17:58 2023

@author: mpingos
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:50:05 2023

@author: mpingos
"""

import re
import os
import time
import psutil  # for CPU usage tracking

# Function to process TTL data for user-defined tags and organize by values
def process_chunk(chunk, tags, folder_name):
    # Split TTL data into individual sources
    sources = re.split('\n\n+', chunk)

    # Extract sources based on user-defined tags and values
    for source in sources:
        match_tags = [re.search(r'{} "([^"]+)"'.format(re.escape(tag)), source) for tag in tags]
        if all(match_tags):
            tag_values = [match.group(1) for match in match_tags]

            # Create folders for each tag value
            folder_path = folder_name
            for i, tag_value in enumerate(tag_values):
                tag_folder = os.path.join(folder_path, tag_value.lower() + '_subfolder')
                if not os.path.exists(tag_folder):
                    os.makedirs(tag_folder)
                folder_path = tag_folder

                # Save the source in the corresponding TTL file with an empty line after each source
                level_ttl = '\n\n'.join([source.strip() + '\n'])
                level_filename = os.path.join(tag_folder, '{}_level_sources.ttl'.format(tags[i].lower()))
                with open(level_filename, 'a') as file:
                    file.write(level_ttl)

                print('TTL file for {} with values {} saved in folder {}'.format(tags[:i+1], tag_values[:i+1], tag_folder))

def read_in_chunks(file_object, chunk_size=1024*1024):
    """Lazy function to read a file piece by piece."""
    while True:
        chunk = file_object.read(chunk_size)
        if not chunk:
            break
        yield chunk

# Main script starts here
user_tags = raw_input("Enter the tags separated by spaces: ").split()
file_path = raw_input("Enter the file path for the TTL data: ")

folder_name = '_'.join(user_tags).lower() + '_folder'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

start_time = time.time()
start_cpu = psutil.cpu_percent(interval=None)  # Start CPU usage measurement

with open(file_path, 'r') as file:
    for chunk in read_in_chunks(file):
        process_chunk(chunk, user_tags, folder_name)

end_cpu = psutil.cpu_percent(interval=None)  # End CPU usage measurement
end_time = time.time()

elapsed_time = end_time - start_time
cpu_usage = end_cpu - start_cpu

print('\nExecution time: {:.4f} seconds'.format(elapsed_time))
print('Approximate CPU usage: {:.2f}%'.format(cpu_usage))