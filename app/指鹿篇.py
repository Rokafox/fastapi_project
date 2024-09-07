"""
趙高欲為亂、恐群臣不聽、乃先設驗。持鹿獻於二世、曰「馬也。」二世笑曰、「丞相誤邪。謂鹿為馬。」問左右。
左右或默、或言馬以阿順趙高、或言鹿。高因陰中諸言鹿者以法。後群臣皆畏高。

宦官の趙高が、政治を簒奪しようと企んだが、群臣が従わないのに用心して、まず試してみることとした。
二世皇帝胡亥に鹿を献上して「馬です」と言った。皇帝は笑って「丞相よ、間違っているよ。鹿を馬と言っている」と言った。
そしてそこにいた家臣たちに聞いた。家臣らは、おし黙る者あり、中には趙高に阿って馬という者もいたが、鹿と言ったものもいた。
趙高は鹿と言った者を法に引っ掛けてひそかに陥れた。その後、群臣は趙高を恐れしたがった。
"""


def 日本語になーれ(inputstring : str) -> str:
    """
    鹿よ、馬に！
    """
    match inputstring:
        case "Invalid credentials":
            return "資格情報が無効です"
        case "Creation failed: String should have at least 4 characters":
            return "作成失敗: 文字列は少なくとも4文字でなければならない"
        case "Creation failed: User with the same name already exists!":
            return "作成失敗: 同じ名のユーザーがすでに存在します"
        case "User created successfully!":
            return "ユーザーが正常に作成されました"
        case "Project created successfully!":
            return "プロジェクトが正常に作成されました"
        case "Creation Failed: Project with the same name already exists!":
            return "作成失敗: 同じ名前のプロジェクトがすでに存在します"
        case _:
            return f"日本語になーれ()に未対応の文字列が渡されました: {inputstring}"