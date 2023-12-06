# Register the submod
init -990 python:
    store.mas_submod_utils.Submod(
        author="N3xtery",
        name="Durak",
        description="Play the Durak card game with your Monika!",
        version="1.0.0",
        dependencies={},
        settings_pane=""
    )

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Durak",
            user_name="N3xtery",
            repository_name="MAS-Submod-Durak",
            submod_dir="/Submods/Durak"
        )