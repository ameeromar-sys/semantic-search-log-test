import re

input_file = "data/HDFS.log"
output_file = "data/clean_logs.txt"

clean_logs = []

with open(input_file) as f:
    for line in f:

        # remove timestamp at start
        line = re.sub(r'^\d+\s+\d+\s+\d+\s+', '', line)

        # remove block ids
        line = re.sub(r'blk_-?\d+', 'block', line)

        # remove IP addresses
        line = re.sub(r'\d+\.\d+\.\d+\.\d+(:\d+)?', 'ip', line)

        # remove file paths
        line = re.sub(r'/[\w/.\-]+', 'path', line)

        # remove java class names
        line = re.sub(r'\b[\w]+\.[\w.$]+\b', '', line)

        # remove extra spaces
        line = re.sub(r'\s+', ' ', line).strip()

        # remove log level
        line = re.sub(r'\b(INFO|WARN|ERROR|DEBUG)\b', '', line)

        # remove special characters
        line = re.sub(r'[:*]', ' ', line)

        # remove numbers
        line = re.sub(r'\b\d+\b', '', line)

        # normalize placeholders
        line = line.replace("src", "source")
        line = line.replace("dest", "destination")

        # remove duplicate words
        words = line.split()
        line = " ".join(dict.fromkeys(words))

        # remove extra spaces
        line = re.sub(r'\s+', ' ', line).strip()

        if len(line) > 10:
            clean_logs.append(line)

with open(output_file, "w") as f:
    for log in clean_logs:
        f.write(log + "\n")

print("Clean logs:", len(clean_logs))