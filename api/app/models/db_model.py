from dataclasses import dataclass


@dataclass
class EpisodeCol:
    episode_id: str = "episode_id"
    episode_name: str = "episode_name"


@dataclass
class CharacterCol:
    character_id: str = "character_id"
    character_name: str = "character_name"


@dataclass
class EpisodeCharacterAppearanceCol:
    character: str = "character"
    episode: str = "episode"


@dataclass
class CommentCol:
    comment_id: str = "comment_id"
    comment_content: str = "comment_content"


@dataclass
class EpisodeCommentCol:
    comment_id: str = "comment_id"
    episode_id: str = "episode_id"


@dataclass
class CharacterCommentCol:
    comment_id: str = "comment_id"
    character_id: str = "character_id"


@dataclass
class EpisodeCharacterAppearanceCommentCol:
    comment_id: str = "comment_id"
    character: str = "character"
    episode: str = "episode"


@dataclass
class TableNames:
    comment: str = "comment"
    episode: str = "episode"
    character: str = "character"
    episode_character_appearance: str = "episode_character_appearance"

    # Comment
    episode_comment: str = "episode_comment"
    character_comment: str = "character_comment"
    episode_character_appearance_comment: str = "episode_character_appearance_comment"


@dataclass
class Table:
    names = TableNames

    # Episode and character
    episode_col_names = EpisodeCol
    character_col_names = CharacterCol
    episode_character_appearance_col_names = EpisodeCharacterAppearanceCol

    # Comment
    comment_col_names = CommentCol
    episode_comment_col_names = EpisodeCommentCol
    character_comment_col_names = CharacterCommentCol
    episode_character_appearance_comment_col_names = (
        EpisodeCharacterAppearanceCommentCol
    )
