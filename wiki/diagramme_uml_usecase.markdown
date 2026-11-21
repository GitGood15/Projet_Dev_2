L’intelligence artificielle a été utilisée comme outil d’assistance pour contribuer à la reformulation de certaines phrases, dans le but d’améliorer la clarté et la cohérence du document.
```mermaid
flowchart LR
    subgraph App ["Application de gestion d'une soirée quiz"]
        F01(["F-01 Gérer les équipes"])
        F02(["F-02 Gérer et importer les questions"])
        F03(["F-03 Organiser une soirée"])
        F04(["F-04 Encoder les scores et résultats"])
        F05(["F-05 Consulter le classement d'une soirée"])
        F06(["F-06 Gérer le championnat annuel"])
        F07(["F-07 Gérer les manches à miser"])
        F08(["F-08 Sauvegarder et restaurer les données"])
        F09(["F-09 Annuler la dernière modification"])
    end

    Mertens["👤 M. Mertens (Gérant)"] --- F01
    Mertens --- F02
    Mertens --- F03
    Mertens --- F04
    Mertens --- F05
    Mertens --- F06
    Mertens --- F07
    Mertens --- F08
    Mertens --- F09
```
* **Identification de l'acteur :** Sur le diagramme, un seul acteur est représenté : M. Mertens. Les équipes et les capitaines participent au quiz sur papier et échangent directement avec lui. Comme le programme fonctionne sur l'ordinateur du café et que seul M. Mertens l'utilise, il est donc le seul acteur qui interagit directement avec le système informatique.
* **Délimitation du système :** Le cadre autour du diagramme représente les limites de l'application que nous devons développer. Powerpoint et clés USB sont considérés comme des outils externes. Ils ne sont donc pas représentés comme des acteurs du système.
* **Nommage et organisation des cas d'utilisation :** Les cas d'utilisation sont formulés avec des verbes à l'infinitif afin de bien montrer les actions réalisées par l'utilisateur. Ils font également référence aux éléments du cahier des charges grâce à leur numéro (F-xx).