coords_of_Aroma_markets = [
    [42.44743, 19.25001],
    [42.45004, 19.23621],
    [42.43793, 19.23752],
    [42.42672, 19.24672],
    [42.42758, 19.25225],
    [42.42815, 19.27409],
    [42.43395, 19.28076],
    [42.43547, 19.2778],
    [42.44166, 19.26338],
    [42.44355, 19.25267],
    [42.44159, 19.25163]
]

coords_of_Franca_markets = [
    [42.45401, 19.26063],
    [42.44522, 19.25504],
    [42.45151, 19.23678],
    [42.43805, 19.22601],
    [42.43059, 19.25742],
    [42.43358, 19.26262],
    [42.43556, 19.28016],
    [42.43782, 19.27726],
]

coords_of_Voli_markets = [
    [42.44953, 19.25939],
    [42.44769, 19.24537],
    [42.44712, 19.24267],
    [42.44924, 19.23057],
    [42.43778, 19.2321],
    [42.42913, 19.27182],
    [42.44252, 19.27376],
    [42.4443, 19.25227],
    [42.4421, 19.24817],
    [42.44128, 19.2529],
    [42.44042, 19.26387],
    [42.43491, 19.26032],
]

tree_of_categories = {
    'meat_category':
        {
            'pork':
                {
                    'Aroma':
                        ["empty"],
                    'Franca':
                        ["Svinjsko meso"],
                    'Voli':
                        ["Svinjetina"]
                },
            'beef':
                {
                    'Aroma':
                        ["empty"],
                    'Franca':
                        ["Juneće meso"],
                    'Voli':
                        ["Junetina"]
                },
            'chicken':
                {
                    'Aroma':
                        ["empty"],
                    'Franca':
                        ["Pileće meso"],
                    'Voli':
                        ["Piletina", "Piletina smrznuto", "Ćuretina smrznuto"]
                },
            'veal':
                {
                    'Aroma':
                        ["empty"],
                    'Franca':
                        ["Teleće meso"],
                    'Voli':
                        ["Teletina"]
                },
            'semi-finished products':
                {
                    'Aroma':
                        ["Suhomesnato slajs", "Mini salame, kobasice i virsle", "Pršut,čajna,budimska,suvi vrat,kulen"],
                    'Franca':
                        ["Delikates, mesne prerađevine"],
                    'Voli':
                        ["Roštilj"]
                }
        },
    'milk_category':
        {
            'milk':
                {
                    'Aroma':
                        ["Dugotrajno mlijeko", "Svjeze mlijeko"],
                    'Franca':
                        ["Mlijeko uht", "Mlijeko uht mala pakovanja", "Mlijeko svježe pasterizovano"],
                    'Voli':
                        ["Mlijeko"]
                },
            'cheese':
                {
                    'hard cheese':
                        {
                            'Aroma':
                                ["Tvrdi i polutvrdi sirevi"],
                            'Franca':
                                ["empty"],
                            'Voli':
                                ["Edamer , gauda emental", "Ostali delikatesni sirevi", "Koziji sir & ovčiji sir"]
                        },
                    'melted cheese':
                        {
                            'Aroma':
                                ["Namazni i topljeni sirevi"],
                            'Franca':
                                ["empty"],
                            'Voli':
                                ["Tost & topljeni sirevi"]
                        }
                },
            'jogurt':
                {
                    'Aroma':
                        ["Jogurt", "Voćni jogurt"],
                    'Franca':
                        ["Jogurt", "Jogurt voćni"],
                    'Voli':
                        ["Jogurt kefir i slično"]
                },
            'maslac':
                {
                    'Aroma':
                        ["Maslac"],
                    'Franca':
                        ["Maslac"],
                    'Voli':
                        ["Maslac & margarin"]
                }
        },
    'pekara_category':
        {
            'bread':
                {
                    'Aroma':
                        ["Hljeb dnevni"],
                    'Franca':
                        ["empty"],
                    'Voli':
                        ["Hljeb"]
                },
            'toast and packaged bread':
                {
                    'Aroma':
                        ["Pakovani hljeb", "Dvopek"],
                    'Franca':
                        ["Hljeb pakovani"],
                    'Voli':
                        ["Tost & dvopek hljeb"]
                },
            'cakes and pastries':
                {
                    'Aroma':
                        ["Gotove torte I kolaci"],
                    'Franca':
                        ["Kolači industrijski suhi", "Kolači sveži pakovani", "Kolači sveži suhi"],
                    'Voli':
                        ["Gotove torte i kolači"]
                }
        },
    'fr_veg_nut_category':
        {
            'fruits':
                {
                    'Aroma':
                        ["Svježe voće"],
                    'Franca':
                        ["Voće"],
                    'Voli':
                        ["Voće"]
                },
            'vegetables':
                {
                    'Aroma':
                        ["Svježe povrće"],
                    'Franca':
                        ["Povrće"],
                    'Voli':
                        ["Povrće"]
                },
            'dried fruits':
                {
                    'Aroma':
                        ["Rinfuzno suvo grozdje", "Rinfuzno voće"],
                    'Franca':
                        ["empty"],
                    'Voli':
                        ["Dehidrirano voće"]
                },
            'nuts':
                {
                    'Aroma':
                        ["Rinfuzni pistaci", "Rinfuzni badem", "Rinfuzni ljesnik", "Rinfuzni kikiriki", "Rinfuzni orah"],
                    'Franca':
                        ["empty"],
                    'Voli':
                        ["Orašasti plodovi & sjemenke"]
                }
        }
}

list_of_group_Aroma = [
    "Suhomesnato slajs", "Mini salame, kobasice i virsle",
    "Pršut,čajna,budimska,suvi vrat,kulen",
    "Dugotrajno mlijeko", "Svjeze mlijeko",
    "Tvrdi i polutvrdi sirevi", "Namazni i topljeni sirevi",
    "Jogurt", "Voćni jogurt", "Maslac", "Hljeb dnevni",
    "Pakovani hljeb", "Dvopek", "Gotove torte I kolaci",
    "Svježe voće", "Svježe povrće", "Rinfuzno suvo grozdje",
    "Rinfuzno voće", "Rinfuzni pistaci", "Rinfuzni badem",
    "Rinfuzni ljesnik", "Rinfuzni kikiriki", "Rinfuzni orah"
]
list_of_group_Franca = [
    "Svinjsko meso", "Juneće meso", "Pileće meso", "Teleće meso",
    "Delikates, mesne prerađevine", "Mlijeko uht",
    "Mlijeko uht mala pakovanja", "Mlijeko svježe pasterizovano",
    "Jogurt", "Jogurt voćni", "Maslac", "Hljeb pakovani",
    "Kolači industrijski suhi", "Kolači sveži pakovani",
    "Kolači sveži suhi", "Voće", "Povrće"
]
list_of_group_Voli = [
    "Svinjetina", "Junetina", "Piletina", "Piletina smrznuto",
    "Ćuretina smrznuto", "Teletina", "Roštilj", "Mlijeko",
    "Edamer , gauda emental", "Ostali delikatesni sirevi",
    "Koziji sir & ovčiji sir", "Tost & topljeni sirevi",
    "Jogurt kefir i slično", "Maslac & margarin", "Hljeb",
    "Tost & dvopek hljeb", "Gotove torte i kolači", "Voće",
    "Povrće", "Dehidrirano voće", "Orašasti plodovi & sjemenke"
]