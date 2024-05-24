class Player:
    blanc        = "blanc"
    noir         = "noir"

class Ponctuation:
    space        = "space"
    semicolon    = "semicolon"
    colon        = "colon"
    comma        = "comma"  

class Events:
    capture      = "capture"
    petit_roque  = "petit_roque"
    grand_roque  = "grand_roque"
    echec        = "echec"
    checkmate    = "checkmate"
    nul          = "nul"
    p_reine      = "p_reine"
    p_tour       = "p_tour"
    p_cavalier   = "p_cavalier"
    p_fou        = "p_fou"

class Pieces:
    pion         = "pion"
    cavalier     = "cavalier"
    fou          = "fou"
    tour         = "tour"
    roi          = "roi"
    reine        =  "reine"

class Deplacement:
    aimed_square = "aimed_square"

class Cleaning_ruleset:
    whitespace   = "whitespace"
    comment      = "comment"
    arrow        = "arrow"

class End:
    endgame      = "endgame" 
    nul          = "nul"

LEXEM_RULES = [
    #Whitespaces
    (r"\/\/.*", Cleaning_ruleset.comment),
    (r"[ \t\n]+", Cleaning_ruleset.whitespace),
    (r"-->", Cleaning_ruleset.arrow),
    #Player
    (r"(?i)\bB[ ]*:",Player.blanc),
    (r"(?i)\bN[ ]*:",Player.noir),
    #Pieces
    (r"(?i)\bpion-([A-Ha-h][2-7])(?=[ -])\b",Pieces.pion),   #Jamais dans le premier et dernier rang
    (r"(?i)\bcavalier-([A-Ha-h][1-8])(?=[ -])\b",Pieces.cavalier),
    (r"(?i)\bfou-([A-Ha-h][1-8])(?=[ -])\b",Pieces.fou),
    (r"(?i)\btour-([A-Ha-h][1-8])(?=[ -])\b",Pieces.tour),
    (r"(?i)\broi-([A-Ha-h][1-8])(?=[ -])\b",Pieces.roi),
    (r"(?i)\breine-([A-Ha-h][1-8])(?=[ -])\b",Pieces.reine),
    #Events
    (r"(?i)-capture",Events.capture),
    (r"(?i)-petit_roque",Events.petit_roque),
    (r"(?i)-grand_roque",Events.grand_roque),
    (r"(?i)-echec",Events.echec),
    (r"(?i)-checkmate",Events.checkmate),
    (r"(?i)-nul",Events.nul),
    (r"(?i)-p_reine",Events.p_reine),
    (r"(?i)-p_cavalier",Events.p_cavalier),
    (r"(?i)-p_fou",Events.p_fou),
    (r"(?i)-p_tour",Events.p_tour),
    #Ponctuation
    (r" ",Ponctuation.space),
    (r";",Ponctuation.semicolon),
    (r",",Ponctuation.colon),
    (r":",Ponctuation.comma),
    #Deplacement
    (r"(?i)\b([A-Ha-h][1-8])\b",Deplacement.aimed_square),
    #End
    (r"(?i)\bendgame\b",End.endgame),
    (r"(?i)\nul\b",End.nul)
]