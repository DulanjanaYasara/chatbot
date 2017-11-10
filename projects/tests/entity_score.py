def extract_candidate_features(candidates, doc_text, doc_title, significant_words):
    import collections, math, nltk, re

    candidate_scores = collections.OrderedDict()

    # get word counts for document
    doc_word_counts = collections.Counter(word.lower()
                                          for sent in nltk.sent_tokenize(doc_text)
                                          for word in nltk.word_tokenize(sent))

    for candidate in candidates:

        pattern = re.compile(r'\b' + re.escape(candidate) + r'(\b|[,;.!?]|\s)', re.IGNORECASE)

        # frequency-based
        # number of times candidate appears in document
        cand_doc_count = len(pattern.findall(doc_text))
        # count could be 0 for multiple reasons; shit happens in a simplified example
        if not cand_doc_count:
            print '**WARNING:', candidate, 'not found!'
            continue

        # statistical
        candidate_words = candidate.split()
        max_word_length = max(len(w) for w in candidate_words)
        term_length = len(candidate_words)
        # get frequencies for term and constituent words
        sum_doc_word_counts = float(sum(doc_word_counts[w.lower()] for w in candidate_words))
        try:
            # lexical cohesion doesn't make sense for 1-word terms
            if term_length == 1:
                lexical_cohesion = 0.0
            else:
                lexical_cohesion = term_length * (
                    1 + math.log(cand_doc_count, 10)) * cand_doc_count / sum_doc_word_counts

        except (ValueError, ZeroDivisionError) as e:
            lexical_cohesion = 0.0

        # positional
        # found in title
        in_title = 1 if pattern.search(doc_title) else 0
        # first/last position, difference between them (spread)
        doc_text_length = float(len(doc_text))
        first_match = pattern.search(doc_text)
        abs_first_occurrence = first_match.start() / doc_text_length
        if cand_doc_count == 1:
            spread = 0.0
            abs_last_occurrence = abs_first_occurrence
        else:
            last_match = object
            for x in pattern.finditer(doc_text):
                last_match = x
            abs_last_occurrence = last_match.start() / doc_text_length
            spread = abs_last_occurrence - abs_first_occurrence

        candidate_scores[candidate] = {'term_count': cand_doc_count,
                                       'term_length': term_length, 'max_word_length': max_word_length,
                                       'spread': spread, 'lexical_cohesion': lexical_cohesion,
                                       'in_title': in_title}

    print candidate_scores


doc_title = 'WSO2 Enterprise Integrator Documentation'
doc_text = """Welcome to the WSO2 Enterprise Integrator (WSO2 EI) 6.1.1 documentation! Get started with WSO2 Enterprise Integrator. If you are new to using WSO2 EI, start here: Get familiar with WSO2 EI. Understand the basics of WSO2 EI and its concepts. Use the Quick Start Guide. Get up and running quickly while learning the fundamentals. Try out the Tutorials. Experiment with common usage scenarios. Deep dive into WSO2 EI. Installation Guide. Enterprise Integrator Tooling. Analytics. Product Extensions. Enterprise Integration Patterns. """
candidates = ['WSO2 Enterprise Integrator', 'WSO2 EI', 'documentation', 'WSO2 Enterprise Integrator', 'WSO2 EI',
              'start', 'WSO2 EI', 'basics', 'WSO2 EI', 'concepts', 'Quick Start Guide', 'fundamentals', 'Tutorials',
              'Experiment', 'common usage scenarios', 'Deep dive', 'WSO2 EI', 'Installation Guide',
              'Enterprise Integrator Tooling', 'Analytics', 'Product Extensions', 'Enterprise Integration Patterns']

extract_candidate_features(candidates, doc_text, doc_title)
