import re, sys

# Converts html files with modbus register listing to python code as needed by py-sma-modbus.
# Regex tested with SBxx-1VA-41 and SBS-x.0 files.

if not len(sys.argv) == 2:
    sys.exit("Usage: {} <htmlfile>".format(sys.argv[0]))

try:
    with open(sys.argv[1], 'r') as file:
        html = file.read() #.replace('\n', '')
except:
    sys.exit("Error while opening html file.")

pattern='^<tr><td>(?:<[^>]*>){0,2}(?P<identifier>[A-Za-z0-9-\.]*)(?:</[^>]*>){0,2}</td><td>(?:<[^>]*>){0,2}(?P<register>[0-9]*)(?:</[^>]*>){0,2}</td><td>(?:<[^>]*>){0,2}(?P<length>[0-9]*)(?:</[^>]*>){0,2}</td><td>(?:<[^>]*>){0,2}(?P<type>[A-Za-z0-9]*)(?:</[^>]*>){0,2}</td><td>(?:<[^>]*>){0,2}(?P<format>[A-Za-z0-9_]*)(?:</[^>]*>){0,2}</td>.*<td>(?:<[^>]*>){0,2}(?P<description>[^<]*)(?:</[^>]*>){0,2}</td><td>.*</td></tr>$'

rx = re.compile(pattern, re.MULTILINE)
matches = rx.finditer(html)

cnt=0
for m_idx in matches:
    print("    wr.add_register({}({}, \"{}\", \"{}\"))".format(m_idx.group('type'), m_idx.group('register'), m_idx.group('identifier'), m_idx.group('description')))
    cnt+=1
print ("total: {}".format(cnt))
