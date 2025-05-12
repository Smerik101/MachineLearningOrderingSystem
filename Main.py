selection = int(input("Please Enter Selection - (0 - Stocktake, 1 - Ordering)"))
if selection == 0:
    import stocktake
elif selection == 1:
    import preprocessing
    import modeltraining
    import ordering
