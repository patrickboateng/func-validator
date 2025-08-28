.PHONY: doctest


doctest:
	 python -m doctest -o IGNORE_EXCEPTION_DETAIL -v .\README.md