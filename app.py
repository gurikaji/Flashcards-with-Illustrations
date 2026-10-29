import streamlit as st
from PIL import Image
import csv
import random

st.set_page_config(page_title="イラストフラッシュカード", layout="centered")

st.title("📚 イラストフラッシュカード")

# セッション状態の初期化
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_name" not in st.session_state:
    st.session_state.show_name = False
if "playlist" not in st.session_state:
    st.session_state.playlist = []

# サイドバー：ファイルのアップロード
st.sidebar.header("📁 ファイルの選択")
uploaded_images = st.sidebar.file_uploader(
    "イラスト画像をすべて選択してください（複数可）", 
    type=["png", "jpg", "jpeg", "webp", "gif"], 
    accept_multiple_files=True
)
uploaded_csv = st.sidebar.file_uploader(
    "CSV（またはテキスト）ファイルを選択してください", 
    type=["csv", "txt"]
)

# CSVデータの読み込み
csv_names = []
if uploaded_csv:
    try:
        content = uploaded_csv.getvalue().decode("utf-8-sig")
        reader = csv.reader(content.splitlines())
        for row in reader:
            if not row:
                continue
            name = row[1].strip() if len(row) > 1 else row[0].strip()
            if name:
                csv_names.append(name)
    except Exception as e:
        st.sidebar.error(f"CSVの読み込みエラー: {e}")

if uploaded_images:
    # プレイリストの初期設定
    if not st.session_state.playlist or len(st.session_state.playlist) != len(uploaded_images):
        st.session_state.playlist = list(range(len(uploaded_images)))

    # ランダムボタン
    if st.sidebar.button("🎲 順番をランダムにする"):
        random.shuffle(st.session_state.playlist)
        st.session_state.current_index = 0
        st.session_state.show_name = False
        st.rerun()

    playlist = st.session_state.playlist
    idx = st.session_state.current_index
    total = len(playlist)

    if total > 0:
        file_idx = playlist[idx]
        img_file = uploaded_images[file_idx]

        # 番号付きのヘッダー表示
        st.subheader(f"【 No. {idx + 1} / {total} 】")

        # 画像の表示
        image = Image.open(img_file)
        st.image(image, use_container_width=True)

        # 答え（名前）の表示切り替え
        if st.session_state.show_name:
            if csv_names and file_idx < len(csv_names):
                item_name = csv_names[file_idx]
            else:
                item_name = img_file.name.split('.')[0]
            st.success(f"**【 No. {idx + 1} 】 {item_name}**")
        else:
            st.info("💡下のボタンを押すと、番号と答え（名前）が表示されます。")

        # 操作ボタン
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("◀ 戻る", use_container_width=True):
                if st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
                    st.session_state.show_name = False
                    st.rerun()

        with col2:
            if not st.session_state.show_name:
                if st.button("👁️ 答えを見る", type="primary", use_container_width=True):
                    st.session_state.show_name = True
                    st.rerun()
            else:
                if st.button("▶ 次へ進む", type="primary", use_container_width=True):
                    if st.session_state.current_index < total - 1:
                        st.session_state.current_index += 1
                        st.session_state.show_name = False
                        st.rerun()
                    else:
                        st.balloons()
                        st.success("すべてのカードが終了しました！")

        with col3:
            if st.button("🔄 最初から", use_container_width=True):
                st.session_state.current_index = 0
                st.session_state.show_name = False
                st.rerun()
else:
    st.info("👈 左側のメニューから、イラスト画像とCSVファイルをアップロードしてください。")