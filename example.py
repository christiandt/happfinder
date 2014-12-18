from happfinder import Happfinder, Happening

finder = Happfinder()
happenings = finder.find_happenings(location='Storsalen')

for happening in happenings:
	print happening.summary()