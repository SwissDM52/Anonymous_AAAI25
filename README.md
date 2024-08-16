# Anonymous_AAAI25

## Code File
- crypto.py       ------------------------- Code that implements all core cryptographic functionalities, including key creation, signing, and signature verification.
- bls_bloom.py    ------------------------- Code for text generation in an LLM model that implements BLS watermark embedding and verification functionality.
- dvs_bloom.py    ------------------------- Code for text generation in an LLM model that implements DVS watermark embedding and verification functionality.
- mdvs_bloom.py   ------------------------- Code for text generation in an LLM model that implements MDVS watermark embedding and verification functionality.
- origin_bloom.py ------------------------- Original code for text generation in an LLM model without watermark embedding.

## Example
- python dvs_bloom.py "Please tell me about California's history." 8
- python mdvs_bloom.py "Please tell me about California's history." 16
- python bls_bloom.py "Please tell me about California's history." 24
- python origin_bloom.py "Please tell me about California's history." 48
