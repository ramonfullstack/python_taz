export PYTHONPATH=$PYTHONPATH:$(pwd)

test:
	@SIMPLE_SETTINGS=taz.settings.test py.test -xs .

test-matching:
	@SIMPLE_SETTINGS=taz.settings.test py.test -rxs --pdb -k$(Q) -vv taz
