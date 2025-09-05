#!/usr/bin/env bash

# Declare an array
files=()
directory=""
errors="py_errors.txt"

read -p "Enter path to search for files: " directory

if [ ! -f "$errors" ]; then
    touch "$errors"
fi

# Loop to find python files and add them to the array.
while IFS= read -r item; do
    files+=("$item")
    
# The '< <(command)' syntax is called process substitution. It allows the output of a command (in this case, 'find "$directory" -name "*.py"')
# to be provided as the input to the 'while' or 'done' loop as if it were a file. This is useful for reading command output line-by-line
# without creating a temporary file.
done < <(find "$directory" -name "*.py")

# Loop round each file in the array to run 'pycodesyle' on them
for file in "${files[@]}"; do
    case $file in
        *__init__.py|*/migrations/*|*/tests/*)
            echo "⏩ Skipping $file"
            continue
            ;;
    esac
    while true; do
        if pycodestyle "$file" > "$errors" 2>&1; then
            echo "✅ $file passed style checks"
            echo
            break
        else
            answer=""
            echo "Do you wish to clear the screen?"
            echo "Enter 'Y' for Yes"
            echo "Enter 'N' for No"
            read -r answer
            if [[ $answer == 'Y' || $answer == 'y' ]]; then
                clear
            fi
            echo "Do you want to check the file, $file for correction?"
            echo "Enter 'Y' for Yes"
            echo "Enter 'N' for No"
            read -r answer
            if [[ $answer == 'n' || $answer == 'N' ]]; then
                echo "⏩ Skipping $file"
                break
            fi
            echo "Opening $file in VS Code (style issues found)..."
            code "$file"
            cat $errors
            read -p "Press Enter when you are done editing '$file' to recheck"
            echo
        fi
    done
done

rm "$errors"