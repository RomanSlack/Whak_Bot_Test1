import subprocess


command = [
    'h8mail',
    '-t', 'coolkidswag',
    '-q', 'username',
    '-k', 'dehashed_email=kaidensimon8@gmail.com',
    'dehashed_key=2xiwpa9pnc0j0nhlbmtlwz959o9w6gno'
]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print("Output:", result.stdout)
