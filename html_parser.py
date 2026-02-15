def extract_text(html):
    text = ""
    inside_tag = False
    inside_script = False
    inside_style = False

    i = 0
    while i < len(html):

        # Detect <script>
        if html[i:i+8].lower() == "<script>":
            inside_script = True
            i += 8
            continue

        # Detect </script>
        if html[i:i+9].lower() == "</script>":
            inside_script = False
            i += 9
            continue

        # Detect <style>
        if html[i:i+7].lower() == "<style>":
            inside_style = True
            i += 7
            continue

        # Detect </style>
        if html[i:i+8].lower() == "</style>":
            inside_style = False
            i += 8
            continue

        # Skip script/style content
        if inside_script or inside_style:
            i += 1
            continue

        c = html[i]

        if c == "<":
            inside_tag = True
        elif c == ">":
            inside_tag = False
            text += " "
        elif not inside_tag:
            text += c

        i += 1

    # Clean output
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)
