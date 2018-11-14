import arpa

models = arpa.loadf("/Users/huangruizhe/Downloads/PycharmProjects/lm_adapt/data/c5-end.arpa")
lm = models[0]  # ARPA files may contain several models.

# probability p(end|in, the)
print(lm.p("4 9 5"))
print(lm.log_p("4 9 5"))

# sentence score w/ sentence markers
print(lm.s("4 9 3 4 7 5 7"))
print(lm.log_s("4 9 3 4 7 5 7"))

# sentence score w/o sentence markers
# print(lm.s("4 9 3 4 7 5 7", sos=False, eos=False))
print(lm.log_s("4 9 3 4 7 5 7", sos=False, eos=False))

# entries of order n, e.g. (-0.4317983, ('3', '4'), 0.3461446)
# ref: python-arpa/arpa/models/simple.py
print([e for e in lm._entries(2)])

# vocabularies
print([v for v in lm.vocabulary()])

