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
        case "Creation failed: Username is not allowed to contain english special characters!":
            return "作成失敗: ユーザー名に英語の幾つの特殊文字を含めることはできません"
        case "Creation failed: User with the same name already exists!":
            return "作成失敗: 同じ名のユーザーがすでに存在します"
        case "User created successfully!":
            return "ユーザーが正常に作成されました"
        case "You cannot delete yourself!":
            return "自分を消さないでください"
        case "Project created successfully!":
            return "プロジェクトが正常に作成されました"
        case "Creation Failed: Project with the same name already exists!":
            return "作成失敗: 同じ名前のプロジェクトがすでに存在します"
        case "Creation Failed: Start date is greater than end date!":
            return "作成失敗: 開始日が終了日よりも後になります"
        case "Creation Failed: Start time is greater than end time!":
            return "作成失敗: 開始時間が終了時間よりも後になります"
        case "Creation Failed: One or more user does not exist!":
            return "作成失敗: 存在しないユーザーがいます"
        case "Creation failed: User not found!":
            return "作成失敗： ユーザーが見つかりません"
        case "Creation failed: User is not hiruchaaru!":
            return "作成失敗： ユーザーはヒルチャールではありません"
        case "Creation failed: Project not found!":
            return "作成失敗： プロジェクトが見つかりません"
        # case "Creation failed: Same attendance already exists for \d{4}-\d{2}-\d{2}":
        #     return f"作成失敗: 同じ出勤記録がすでに存在します: {inputstring}"
        case "Attendance created successfully!":
            return "出勤記録が正常に作成されました"
        case "Deletion failed: User not found!":
            return "削除失敗： ユーザーが見つかりません"
        case "Deletion failed: Project not found!":
            return "削除失敗： プロジェクトが見つかりません"
        case "Deletion failed: Attendance not found!":
            return "削除失敗： 出勤記録が見つかりません"
        case "Attendance deleted successfully!":
            return "出勤記録が正常に削除されました"
        case "User deleted successfully!":
            return "ユーザーが正常に削除されました"
        case "Project deleted successfully!":
            return "プロジェクトが正常に削除されました"
        case "Update failed: Project not found!":
            return "更新失敗： プロジェクトが見つかりません"
        case "Update failed: Project with the same name already exists!":
            return "更新失敗: 同じ名前のプロジェクトがすでに存在します"
        case "Project updated successfully!":
            return "プロジェクトが正常に更新されました"
        case "Check-in successful!":
            return "出勤を記録しました"
        case "Check-out successful!":
            return "退勤を記録しました"
        case _:
            final = 今一度日本語になろう(inputstring)
            if not final:
                return f"日本語になーれ()或は今一度日本語になろう()に未対応の文字列が渡されました: {inputstring}"
            return final
        

def 今一度日本語になろう(inputstring: str) -> str:
    if "Creation Failed" in inputstring and "is not a projectmanager!" in inputstring:
        return "作成に失敗しました: {} はプロジェクトマネージャーではありません！".format(
            inputstring.split(" ")[-4]
        )
    return None
