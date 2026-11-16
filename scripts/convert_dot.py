import re
import os
import subprocess
import sys

def process_file(filepath):
    print(f"Processing file: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find {dot} blocks
    dot_pattern = re.compile(r'(```\{dot\}(.*?)```)', re.DOTALL)
    matches = list(dot_pattern.finditer(content))
    matches.reverse() # Process bottom-to-top
    
    filename = os.path.basename(filepath)
    chapter_match = re.search(r'(ch\d+)', filename)
    chapter_dir = chapter_match.group(1) if chapter_match else "general"
    img_dir = os.path.join("images", chapter_dir)
    os.makedirs(img_dir, exist_ok=True)
    
    count = 0
    new_content = content
    
    for match in matches:
        full_block = match.group(0)
        inner_content = match.group(2)
        
        # SKIP if it's deactivated (eval: false)
        if re.search(r'//\|\s*eval:\s*false', inner_content):
            continue
            
        # Extract metadata
        label_match = re.search(r'//\|\s*label:\s*([\w-]+)', inner_content)
        caption_match = re.search(r'//\|\s*fig-cap:\s*"(.*?)"', inner_content)
        width_match = re.search(r'//\|\s*out-width:\s*"(.*?)"', inner_content)
        
        label = label_match.group(1) if label_match else f"fig-dot-{os.urandom(2).hex()}"
        caption = caption_match.group(1) if caption_match else ""
        width = width_match.group(1) if width_match else "60%"
        
        # Extract clean dot code
        dot_lines = []
        options_lines = []
        for line in inner_content.strip().split('\n'):
            if line.strip().startswith('//|'):
                if 'label:' not in line and 'fig-cap:' not in line and 'eval:' not in line and 'echo:' not in line:
                    options_lines.append(line)
            else:
                dot_lines.append(line)
        dot_code = '\n'.join(dot_lines).strip()
        
        svg_filename = f"{label}.svg"
        svg_path = os.path.join(img_dir, svg_filename)
        
        print(f"Updating {label}...")
        
        try:
            result = subprocess.run(['dot', '-Tsvg'], input=dot_code.encode('utf-8'), capture_output=True, check=True)
            with open(svg_path, 'wb') as f:
                f.write(result.stdout)
                
            # Construct replacement parts
            attr_str = f"#{label} width=\"{width}\""
            img_line = f"![{caption}]({os.path.join('images', chapter_dir, svg_filename)}){{{attr_str}}}"
            new_options = ["//| eval: false", "//| echo: false"] + options_lines
            new_block = f"```{{dot}}\n" + "\n".join(new_options) + "\n" + dot_code + "\n```"
            
            # IDEMPOTENT REPLACEMENT: Remove any existing image line for this label above the chunk
            # Regex looks for the specific image pattern for this label
            img_search_pattern = re.compile(r'\!\[.*?\]\(.*?images/' + chapter_dir + '/' + label + r'\.svg\)\{#' + label + r'.*?\}\n*', re.MULTILINE)
            
            # Replace in whole content
            final_replacement = f"{img_line}\n\n{new_block}"
            
            # Find match span in CURRENT new_content
            # Since we iterate reversed, we can find the equivalent start/end
            # but regex search is safer for the image cleanup
            
            start, end = match.span()
            # We first replace the block itself
            new_content = new_content[:start] + final_replacement + new_content[end:]
            
            # Then we clean up any orphaned image lines created by previous runs
            # (In case there are multiple, though there should be only one)
            new_content = img_search_pattern.sub('', new_content, count=1 if count > 0 else 0)
            
            count += 1
        except Exception as e:
            print(f"Error: {e}")

    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Done! Updated {count} graphs.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
