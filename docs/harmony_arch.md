---
title: Harmony arch
author: M. Kroon
---

# C4

```plantuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_LANDSCAPE()

Boundary(cons, "Consortium member", "8x") {
    Person(cons_tech, "Data provider", "")
    Container(cons_db, "Database", "unknown system", "")
    Person(researcher, "Researcher", "")
}

Boundary(dre, "DRE", "Provider?") {
    Person(ds, "Datasteward", "")
    Person(devops, "DevOps", "")

    Container(landingZone, "Landing Zone", "Folder", "8x")
    Container(dataPrep, "Harmonization Zone", "Folder", "8x")
    Container(db, "Integrated data", "JSON/SQLite", "1x")
}

Boundary(hosting, "Data repository", "DANS?") {
    Container(catalogue, "Catalogue", "Dataverse?")
}

Rel(cons_db, landingZone, "import")
Rel(cons_tech, cons_db, "manages")
Rel(cons_tech, landingZone, "Performs upload")

Rel(landingZone, dataPrep, "validation (automatic)")
Rel(dataPrep, db, "integration")

Rel(ds, dataPrep, "Harmonize")
Rel(devops, db, "Performs integration")

Rel(researcher, db, "Analyzes")

Rel(db, catalogue, "Publish")

Person(ext_researcher, "External researcher", "")
Rel(ext_researcher, catalogue, "Requests access")


Person(access_committee, "Access committee", "")
Rel(access_committee, catalogue, "Manages access")

```

