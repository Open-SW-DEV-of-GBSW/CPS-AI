import os

folder_path = 'folder/test/labels'

for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                parts[0] = '0'  # 클래스 번호를 0으로 변경
                new_line = ' '.join(parts)
                new_lines.append(new_line)
        
        with open(file_path, 'w') as f:
            f.write('\n'.join(new_lines))
