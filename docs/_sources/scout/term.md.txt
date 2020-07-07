# Term Functions

Scout provides a set of helper functions for extensibility. These term functions modify the text in the required form.

## Tokenizer
This function returns a list of important words in a text. The input text is converted to all lowercase characters. Special characters and punctuations are removed from the text. Finally, stop words like ‘a’, ‘the’, ‘for’, ‘from’ etc. are removed.

> Note : Hyphenated words are converted to single word. 
For example, `‘un-filtered’` would become `‘unfiltered’`.

## Ngram Generator
Ngram converts a text into a list of smaller text chunks.

The Ngram dictionary contains positions of a word in the paragraph. Below is an example of three words as inferred in the Ngram dict. 

##### Input Word List
```
words = ["change", "changes", "changing"]
```

##### Output Ngram List
```
ngram = { 
   "cha" : [7, 20, 34], 
   "chan" : [7, 20, 34], 
   "chang" : [7, 20, 34], 
   "change" : [7, 20], 
   "changes" : [20], 
   "changi" : [34], 
   "changin" : [34], 
   "changing" : [34]
}
```

## Partition Generator
This function yields a `(word, path)` combo. That is, if a particular word were to be stored, at which location they would be stored and read from. 

```
changlings     idx_sample_db/c/ch/chang_index.json
```