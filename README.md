# Dependencies

```bash
unidecode
emoji
*kenlm
fuzzy
scikit-learn
pyxdameraulevenshtein 
pygtrie
numpy     
```

*Install kenlm wrapper from github:

```bash
pip install https://github.com/kpu/kenlm/archive/master.zip
```

# Usage

```python

    # Load english dictionary
    english_vocab = load_english_vocab(...)
    english_vocab.update(load_english_vocab(...))
    
    # Load bilingual lexicon dictionary
    foreign_dict = load_lexicon_norm(...)
    
    # Load target language model
    lm = kenlm.Model(...)

    # Train a ngram model if needed
    # ngram_train(foreign_dict, 'hin-tfidf-ngram_algo')

    # Ulf's romanizer
    romanizer = partial(romanize,
                        romanization_path=...,
                        language_code="hin")

    soundex_inst = fuzzy.DMetaphone()
    soundex_algo = lambda x: soundex_inst(x)[0].decode('utf-8') if soundex_inst(x)[0] is not None else x
    english_encoded_vocab = {e: soundex_algo(e) for e in english_vocab if e}

    # load the ngram model
    ngram_algo = pickle.loads(open(..., "rb").read())

    soundex_model = partial(soundex_similarity,
                            encoded_english_vocab=english_encoded_vocab,
                            romanizer=romanizer,
                            soundex=soundex_algo)

    lev_model = partial(lev_similarity, backup=soundex_model)
    ngram_model = partial(ngram_similarity, model=ngram_algo, backup=lev_model)
    final_model = partial(exact_similarity, backup=ngram_model)

    for line in open(...):
        source, target = line.strip('\n').split('\t')
        oovs = extract_oov(target, source, english_vocab=english_vocab, romanization=True)
        best, mods = translate_oov(target, oovs, foreign_dict, final_model, lm.score)

        if best != target:

            for oov in oovs:
                alt = list(mods[oov].keys())[0]
                trans = mods[oov][alt]
                debug.debug(f"{romanizer(oov)} -> {romanizer(alt)} : {list(trans)}")

            debug.debug(best)
            debug.debug("*"*100)
```