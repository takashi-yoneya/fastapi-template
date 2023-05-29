from pydantic import BaseModel, Field


class AnalyzedlanguageToken(BaseModel):
    surface: str = Field(..., description="表層形式(入力文字のまま)")
    dictionaly_form: str = Field(..., description="辞書形式")
    reading_form: str = Field(..., description="読みカナ")
    normalized_form: str = Field(..., description="正規化済の形式")
    part_of_speech: tuple[str] = Field(..., description="品詞")
    begin_pos: int = Field(..., description="開始文字番号")
    end_pos: int = Field(..., description="終了文字番号")


class AnalyzedLanguage(BaseModel):
    raw_text: str
    tokens: list[AnalyzedlanguageToken] = []
    excluded_tokens: list[AnalyzedlanguageToken] = []
    during_time: float
