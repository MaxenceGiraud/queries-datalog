#%%
%load_ext autoreload
%autoreload 2

import parser
#%%
ex = parser.query_parse_file("queries/example.query")
cqnotrr = parser.program_parse_file("queries/CQnotRR.query")
rr = parser.program_parse_file("queries/RR.query")
#%%
cqnotrr.is_CQ()
# %%
cqnotrr.is_rangerestricted()
# %%
rr.is_CQ()
# %%
rr.is_rangerestricted()
# %%
