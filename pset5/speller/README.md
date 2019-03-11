# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

It is the longest word in the English language, its length taken as maximum for word storage.

## According to its man page, what does `getrusage` do?

getrusage() returns resource usage measures

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Because if structure passed by value then new same structure must be created in stack.
This is relative big amount of data and this kind of operation may affect memory usage and common program execution time.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

MainLoop: Read one by one symbol from file until  reached EOF
            if current symbol is aplhabetical or (apostroph and not first character in current word)
                then add current symbol to current word and increment words symbol index
                   if words symbols index becomes greater than max allowed word length
                        skip all readed symbols until reached EOF or non alphabetical symbol
                        reset in word characters index to 0
            else if current symbol is number
                skip all symbols untill EOF or non alphabetical or numeric symbol reached
                reset in word characters index to 0
            else if current symbol is not number or alphabetical or apostroph
                then reached end of current word
                to current word end added \0 symbol
                increments words counter
                performs words spellcheck
                in word characters index resets to 0

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

scanf with %s modifier - read string till space without length control
also to control numbers and apostrophes in words needs additional words handling after reading from file

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

Because passed arguments in this case is readonly and const modifier prevent accidental data changing
