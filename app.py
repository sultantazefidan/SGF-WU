import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_all_results
from main import PasswordTest, HabitsTest, ScoreResult, FeedbackService, hash_password
from db import login, register, save_result, get_results
from datetime import datetime
import plotly.express as px

password_test = PasswordTest()
habits_test = HabitsTest()
feedback_service = FeedbackService()

st.set_page_config(
    page_title="Siber Güvenlik Farkındalık Uygulaması",
    page_icon="🔐",
    layout="centered"
)


def show_app_header():
    st.markdown("""
<div style="text-align:center; margin-top:-30px; margin-bottom:10px;">
    <h1 style="
    text-align:center;
    font-weight:900;
    font-size:38px;
    background: linear-gradient(90deg, #1d4ed8, #4f46e5, #1d4ed8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(0, 198, 255, 0.4);
      ">
     Siber Güvenlik Farkındalık Uygulaması
    </h1>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="
    text-align:center;
    margin-top:6px;
    font-size:17px;
    color:#9AA4BF;
">
    Şifre güvenliğini analiz et, siber farkındalığını artır.
</div>
""", unsafe_allow_html=True)


# UI
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white !important;
    font-weight: 700;
}

label, p, div, span {
    color: white;
}

/* BUTONLAR TAM GENİŞLİK */
div.stButton > button {
    width: 100% !important;
    display: block !important;
    text-align: center !important;

    background-color: #6C63FF;
    color: white;
    border-radius: 10px;
    padding: 12px;
    border: none;
    font-weight: 600;
}

/*  BUTON WRAPPER */
div[data-testid="stButton"] {
    width: 100% !important;
    margin-top: 10px;
}

/*  REGISTER BUTONU */
div[data-testid="stButton"]:nth-of-type(2) button {
    background-color: transparent !important;
    border: 1px solid #6C63FF !important;
    color: white !important;
}

/*  INPUT FULL WIDTH */
.stTextInput > div {
    width: 100% !important;
}

/*  INPUT STYLE */
.stTextInput > div > div > input {
    background-color: #1E1E2F;
    color: white;
    border-radius: 10px;
}

/*  HOVER */
div.stButton > button:hover {
    background-color: #5a52e0;
    color: white;
}

/* SELECT */
div[data-baseweb="select"] > div {
    background-color: #1E1E2F !important;
    color: white !important;
}

/* METRİK */
[data-testid="stMetricValue"] {
    color: white;
}

[data-testid="stMetricLabel"] {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# session state
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "password_result" not in st.session_state:
    st.session_state.password_result = None

if "password_done" not in st.session_state:
    st.session_state.password_done = False

if "habits_score" not in st.session_state:
    st.session_state.habits_score = None

if "risk" not in st.session_state:
    st.session_state.risk = None

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "show_settings_menu" not in st.session_state:
    st.session_state.show_settings_menu = False

def reset_user_flow():
    st.session_state.password_result = None
    st.session_state.password_done = False
    st.session_state.habits_score = None
    st.session_state.risk = None
    st.session_state.result_saved = False


def do_logout():
    st.session_state.page = "login"
    st.session_state.user_id = None
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.show_settings_menu = False
    st.session_state.question_index = 0
    st.session_state.go_test = False
    reset_user_flow()


# login
if st.session_state.page == "login":
    st.markdown("""
    <style>
    /* PREMIUM GRADIENT */
    .stApp {
        background: linear-gradient(135deg, #0E1117 40%, #1f2a4d 100%);
    }

    /* Başlık net beyaz*/
    h1 {

        color: white !important;
        text-align: center;
    }

    /* INPUT FOCUS EFFECT */
    .stTextInput input:focus {
        border: 1px solid #6C63FF !important;
        box-shadow: 0 0 15px rgba(108, 99, 255, 0.5);
    }

    /*  LOGIN KART (ANA PANEL) */
    .block-container {
        background: rgba(17, 21, 39, 0.85); 
        padding: 35px;
        border-radius: 20px;

        max-width: 590px;
        margin: auto;

        box-shadow: 0 0 40px rgba(108, 99, 255, 0.25);
        backdrop-filter: blur(10px); 
    }

    /* INPUT FULL WIDTH */
    .stTextInput {
        width: 100%;
    }

    /* BUTON FULL WIDTH + ORTALI */
    div[data-testid="stButton"] {
        width: 100%;
    }

    .stButton > button {
        width: 100%;
        text-align: center;
        border-radius: 10px;
        padding: 12px;
        font-weight: 600;
    }

    /* PRIMARY BUTTON */
    .stButton > button:first-child {
        background-color: #6C63FF;
        color: white;
    }

    /* SECONDARY BUTTON */
    .stButton > button:last-child {
        background-color: transparent;
        border: 1px solid #6C63FF;
        color: white;
    }

    /* BOŞLUK AYARI */
   .stButton {
        margin-top: 3px !important;
    }

    .stButton > button {
    transition: all 0.3s ease;
}

   .stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 15px rgba(108, 99, 255, 0.5);
    }

    .stTextInput input:focus {
    border: 1px solid #6C63FF !important;
    box-shadow: 0 0 25px rgba(108, 99, 255, 0.7);
    transform: scale(1.02);
    transition: 0.2s;
}

   .stTextInput input:hover {
    box-shadow: 0 0 10px rgba(108, 99, 255, 0.4);
}
.stTextInput input {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
    </style>
    """, unsafe_allow_html=True)

    show_app_header()
    st.markdown("<h2 style='text-align:center; color:white;'>🔐 Giriş</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Kullanıcı Adı", key="login_username")
        password = st.text_input("Şifre", type="password", key="login_password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Giriş Yap", use_container_width=True):
            if not username or not password:
                st.warning("Kullanıcı adı ve şifre zorunlu!")
            else:
                hashed = hash_password(password)
                result = login(username, hashed)

                if result:
                    user_id, role = result

                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.role = role

                    if role == "admin":
                        st.session_state.page = "admin"
                    else:
                        st.session_state.page = "user"

                    st.rerun()
                else:
                    st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, rgba(255,70,70,0.14), rgba(255,120,120,0.08));
                        border: 1px solid rgba(255, 90, 90, 0.28);
                        color: #ffe3e3;
                        padding: 14px 16px;
                        border-radius: 14px;
                        margin-top: 12px;
                        box-shadow: 0 0 12px rgba(255, 80, 80, 0.08);
                        font-size: 15px;
                    ">
                        <span style="font-size:18px; margin-right:8px;">⚠️</span>
                        Giriş başarısız. Bilgilerinizi kontrol edip tekrar deneyin.
                    </div>
                    """, unsafe_allow_html=True)


        if st.button("Yeni kullanıcı kaydı oluştur", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

        if st.button("Şifremi Unuttum", use_container_width=True):
            st.session_state.page = "forgot_password"
            st.rerun()

# register
elif st.session_state.page == "register":
    st.markdown("""
    <style>

    /*ARKA PLAN */
    .stApp {
        background: linear-gradient(135deg, #0E1117 40%, #1f2a4d 100%);
    }

    /* BAŞLIK */
    h1 {
        color: white !important;
        text-align: center;
    }

    /* KART */
    .block-container {
        background: rgba(17, 21, 39, 0.85);
        padding: 35px;
        border-radius: 20px;

        max-width: 570px;
        margin: auto;

        box-shadow: 0 0 40px rgba(108, 99, 255, 0.25);
        backdrop-filter: blur(10px);
    }

    /*INPUT FULL */
    .stTextInput {
        width: 100%;
    }

    /* BUTON FULL + ORTA */
    div[data-testid="stButton"] {
        width: 100%;
    }

    .stButton > button {
        width: 100%;
        text-align: center;
        border-radius: 10px;
        padding: 12px;
        font-weight: 600;
    }

    /*PRIMARY */
    .stButton > button:first-child {
        background-color: #6C63FF;
        color: white;
    }

    /* SECONDARY */
    .stButton > button:last-child {
        background-color: transparent;
        border: 1px solid #6C63FF;
        color: white;
    }

    /* BUTON ARASI BOŞLUK */
    div[data-testid="stButton"] {
        margin-top: 12px;
    }

    h1 {
    font-size: 38px !important;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    }
    .stTextInput input {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

    </style>
    """, unsafe_allow_html=True)
    show_app_header()
    st.markdown("<h4 style='text-align:center; color:white;'>📝 Yeni Kullanıcı Kaydı Oluştur</h3>",
                unsafe_allow_html=True)
    import re

    username = st.text_input("Kullanıcı Adı", key="register_username")

    email = st.text_input("Email", key="register_email")
    email_valid = False
    if email:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.success("Geçerli email ✅")
            email_valid = True
        else:
            st.error("Geçersiz email ❌")
            email_valid = False

    password = st.text_input("Şifre", type="password", key="register_password")

    # Şifre analizi
    if password:
        score = 0

        if len(password) >= 8:
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*" for c in password):
            score += 1

        if score == 1:
            st.progress(25)
            st.warning(
                "Parola güvenlik düzeyi düşüktür. Daha uzun bir parola ile büyük harf, rakam ve özel karakter kullanılması önerilir."
            )

        elif score == 2:
            st.progress(50)
            st.info(
                "Parola güvenlik düzeyi orta seviyededir. Güvenliği artırmak için parola karmaşıklığı geliştirilebilir."
            )

        elif score == 3:
            st.progress(75)
            st.success(
                "Parola güvenlik düzeyi iyidir. Düzenli parola güncellemesi ve benzersiz parola kullanımı önerilir."
            )

        elif score == 4:
            st.progress(100)
            st.success(
                "Parola güvenlik düzeyi yüksektir. Parola güçlü güvenlik kriterlerini karşılamaktadır."
            )

    # demografik bilgiler
    age_group = st.selectbox(
        "Yaş Grubu",
        ["7-17","18-25", "26-40", "41-64", "65+"]
    )

    education_level = st.selectbox(
        "Eğitim Durumu",
        ["Lise ve Altı", "Üniversite Öğrencisi", "Lisans Mezunu", "Yüksek Lisans/Doktora"]
    )

    occupation = st.selectbox(
        "Meslek Grubu",
        ["Öğrenci", "Beyaz Yakalı", "Mavi Yakalı", "Emekli", "Diğer"]
    )

    custom_occupation = ""

    if occupation == "Diğer":
        custom_occupation = st.text_input("Mesleğinizi Yazınız")

    # KAYIT BUTONU
    if st.button("Kaydı Tamamla", use_container_width=True):

        if not username or not email or not password:
            st.warning("Tüm alanları doldurunuz!")

        elif not email_valid:
            st.error("Lütfen geçerli bir email giriniz ❌")

        elif username == "admin":
            st.error("Bu kullanıcı adı kullanılamaz.")

        else:

            if occupation == "Diğer":
                final_occupation = custom_occupation
            else:
                final_occupation = occupation

            hashed = hash_password(password)

            register_success = register(
                username,
                email,
                hashed,
                age_group,
                education_level,
                final_occupation
            )

            if register_success:
                st.balloons()
                st.success("Kayıt başarılı! 🎉")
                st.toast("Artık giriş yapabilirsin 🚀")

                st.session_state.page = "login"
                st.rerun()

            else:
                st.error("❌ Bu kullanıcı adı zaten kayıtlı.")

    # GERİ DÖN BUTONU
    if st.button("Giriş Ekranına Geri Dön", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()



# user panel
if "show_settings_menu" not in st.session_state:
    st.session_state.show_settings_menu = False

if st.session_state.page == "user":
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "go_test" not in st.session_state:
        st.session_state.go_test = False

    st.markdown("""
    <style>

    .stApp {
    background: radial-gradient(
        circle at center,
        #dbeafe 0%,
        #bfdbfe 30%,
        #eaf3ff 60%,
        #f8fbff 100%
    );
}

.stApp::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle, rgba(59,130,246,0.08), transparent 70%);
    filter: blur(40px);
    pointer-events: none;
}
    label, p, div, span, h1, h2, h3 {
        color: #0E1117 !important;
    }

    .block-container {
        max-width: 900px;
        margin: auto;
    }

    .user-card {
        background: rgba(255,255,255,0.65);
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(80, 120, 200, 0.12);
        margin-bottom: 20px;
    }

    .stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
}

.stButton > button {
    background: linear-gradient(90deg, #6C63FF, #7b61ff);
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton > button:hover {
    box-shadow: 0 0 15px rgba(123, 97, 255, 0.6);
    transform: scale(1.02);
}

    </style>
    """, unsafe_allow_html=True)

    show_app_header()

    col_left, col_right = st.columns([13, 1])

    with col_left:
        st.markdown(f"""
        <h2 style="
            margin-top:10px;
            font-weight:700;
            font-size:26px;
        ">
            👤 Hoşgeldin, {st.session_state.username}
        </h2>
        """, unsafe_allow_html=True)

    with col_right:
        if st.button("⚙️", key="settings_toggle"):
            st.session_state.show_settings_menu = not st.session_state.show_settings_menu
            st.rerun()

    if st.session_state.show_settings_menu:
        _, menu_col = st.columns([10, 3])
        with menu_col:
            st.markdown("""
            <style>
            div[data-testid="stVerticalBlock"] div[data-testid="stButton"]:nth-of-type(2) button,
            div[data-testid="stVerticalBlock"] div[data-testid="stButton"]:nth-of-type(3) button {
                background: white !important;
                color: #1e1e1e !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 8px !important;
                font-size: 14px !important;
                text-align: left !important;
                padding: 8px 12px !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.10);
            }
            div[data-testid="stVerticalBlock"] div[data-testid="stButton"]:nth-of-type(2) button:hover,
            div[data-testid="stVerticalBlock"] div[data-testid="stButton"]:nth-of-type(3) button:hover {
               background: #f1f5ff !important;
            }
            </style>
            """, unsafe_allow_html=True)
            if st.button("🔑 Şifre Değiştir", use_container_width=True, key="menu_change_pw"):
                st.session_state.show_settings_menu = False
                st.session_state.page = "change_password"
                st.rerun()
            if st.button("🚪 Çıkış Yap", use_container_width=True, key="menu_logout"):
                do_logout()
                st.rerun()

    st.markdown("""
     <div class="user-card">
          <p style="margin:0; font-size:16px; line-height:1.7; color:#0E1117;">
                  Bu uygulama, kullanıcıların şifre güvenliğini ve dijital alışkanlıklarını değerlendirerek siber güvenlik farkındalık düzeyini analiz etmek amacıyla geliştirilmiştir. 
                  Kullanıcılardan yaş grubu, eğitim durumu ve meslek bilgileri alınarak demografik karşılaştırmalar yapılabilmekte, farklı kullanıcı gruplarının siber güvenlik farkındalık düzeyleri analiz edilebilmektedir.
                  Aşağıdaki adımları tamamlayarak mevcut güvenlik seviyenizi görebilir ve daha güvenli dijital davranışlar için geri bildirim alabilirsiniz.
              </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.go_test:
        st.markdown("""
        <h2 style="
            margin-top:10px;
            font-weight:700;
            font-size:24px;
        ">
        🔐 Şifre Analizi
        </h2>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([5, 1])

        with col1:
            password_input = st.text_input("Şifre Gir", type="password", key="analysis_password")

        with col2:
            st.markdown("""
            <style>
            div.stButton > button {
                margin-top: -4px;
            }
            </style>
            """, unsafe_allow_html=True)

            if st.button("🔍 Analiz Et"):
                if not password_input:
                    st.warning("Lütfen analiz için bir şifre giriniz.")
                else:
                    result = password_test.evaluate(password_input)
                    st.session_state.password_result = result
                    st.session_state.password_done = True

    if st.session_state.password_done and st.session_state.password_result is not None and not st.session_state.go_test:
        result = st.session_state.password_result

        st.success("Analiz tamamlandı !")
        st.write(f"**Skor:** {result['score'] * 20}")
        st.write(f"**Seviye:** {result['level']}")

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #eef4ff, #e0ecff);
            padding: 18px;
            border-radius: 14px;
            margin-top: 10px;
            border-left: 4px solid #6C63FF;
        ">
            <p style="margin:0; font-size:15px;">
                👉 Şimdi güvenlik testine geçerek günlük internet alışkanlıklarını değerlendirebilirsin.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if not st.session_state.go_test:
            if st.button("🚀 Güvenlik Testine Geç", use_container_width=True):
                st.session_state.go_test = True
                st.rerun()

    if st.session_state.go_test:

     st.subheader("🧠 Güvenlik Testi")

     questions = habits_test.getQuestions()

     st.progress((st.session_state.question_index + 1) / len(questions))
     st.caption(f"Soru {st.session_state.question_index + 1} / {len(questions)}")

     q, correct, info = questions[st.session_state.question_index]

     st.markdown(f"""
     <div class="user-card">
         <b>{q}</b>
     </div>
     """, unsafe_allow_html=True)

     st.markdown(f"""
     <div style="
     background:#eef4ff;
     padding:12px;
     border-radius:10px;
     border-left:4px solid #6C63FF;
     margin-top:10px;
     margin-bottom:10px;
     font-size:14px;
     ">
     ℹ️ <b>Kavram Açıklaması:</b><br>
     {info}
     </div>
     """, unsafe_allow_html=True)

     answer = st.radio(
         "",
         ["Evet", "Hayır"],
         key=f"question_{st.session_state.question_index}"
     )

     if answer is not None:
         st.session_state.answers[st.session_state.question_index] = answer

     col1, col2, col3 = st.columns([1, 6, 1])

     with col1:
         if st.session_state.question_index > 0:
             if st.button("⬅️ Geri", use_container_width=True):
                 st.session_state.question_index -= 1
                 st.rerun()

     with col3:
         if st.session_state.question_index < len(questions) - 1:
             if st.button("İleri ➡️", use_container_width=True):
                 st.session_state.question_index += 1
                 st.rerun()

     if st.session_state.question_index == len(questions) - 1:
         if st.button("✅ Testi Bitir", use_container_width=True):

             score = 0

             for i, (q, correct, info) in enumerate(questions):
                 ans = st.session_state.answers.get(i)

                 if (ans == "Evet" and correct == "e") or \
                         (ans == "Hayır" and correct == "h"):
                     score += 1

             risk = habits_test.assessRisk(score)

             st.session_state.habits_score = score
             st.session_state.risk = risk
             st.session_state.page = "result"
             st.rerun()


# change pasword
elif st.session_state.page == "change_password":
    show_app_header()

    st.markdown("### 🔑 Şifre Değiştir")

    old_password = st.text_input("Eski Şifre", type="password")
    new_password = st.text_input("Yeni Şifre", type="password")

    col1, spacer, col2 = st.columns([1, 5, 1])

    with col1:
        if st.button("Güncelle"):
            if not old_password or not new_password:
                st.warning("Tüm alanları doldur!")
            else:
                from db import login, update_password

                username = st.session_state.username

                old_hashed = hash_password(old_password)
                user = login(username, old_hashed)

                if user:
                    new_hashed = hash_password(new_password)
                    update_password(username, new_hashed)

                    st.success("Şifre güncellendi ✅")
                    st.session_state.page = "user"
                    st.rerun()
                else:
                    st.error("Eski şifre yanlış ❌")

    with col2:
        if st.button("⬅️ Geri"):
            st.session_state.show_settings_menu = False
            st.session_state.page = "user"
            st.rerun()
# şifremi unuttum

elif st.session_state.page == "forgot_password":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0E1117 40%, #1f2a4d 100%);
    }

    .block-container {
        background: rgba(17, 21, 39, 0.85);
        padding: 35px;
        border-radius: 20px;
        max-width: 590px;
        margin: auto;
        box-shadow: 0 0 40px rgba(108, 99, 255, 0.25);
        backdrop-filter: blur(10px);
    }

    .stTextInput {
        width: 100%;
    }

    .stTextInput input {
        background-color: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
    }

    div[data-testid="stButton"] {
        width: 100%;
        margin-top: 10px;
    }

    .stButton > button {
    width: 110%;
    border-radius: 10px;
    padding: 12px;
    font-weight: 600;
    background-color: #6C63FF;
    color: white;
    border: none;

    height: 52px;

    display: flex;
    align-items: center;     /* dikey ortala */
    justify-content: center; /* yatay ortala */

    white-space: nowrap;     /* satır kırılmasını engeller */
}
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(108, 99, 255, 0.5);
    }
    .stButton {
    transform: translateX(10px);  /* sağa kaydır */
}
    </style>
    """, unsafe_allow_html=True)

    show_app_header()
    st.markdown("<h3 style='text-align:center;'>🔑 Şifre Sıfırlama</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Kullanıcı Adı")
        # old_password = st.text_input("Eski Şifre", type="password")
        new_password = st.text_input("Yeni Şifre", type="password")

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Güncelle", use_container_width=True):

                from db import update_password, get_user

                if username.strip() == "" or not new_password:
                    st.markdown("""
                                        <div style="
                                            background: linear-gradient(135deg, rgba(255,180,0,0.2), rgba(255,140,0,0.1));
                                            border: 1px solid rgba(255,180,0,0.4);
                                            color: #ffe9c6;
                                            padding: 20px;
                                            border-radius: 16px;
                                            font-size: 15px;
                                            margin-top: 10px;
                                            width: 260%;
                                            box-shadow: 0 0 15px rgba(255,180,0,0.15);
                                        ">
                                        ⚠️ Tüm alanların doldurulması gerekir
                                        </div>
                                        """, unsafe_allow_html=True)

                elif len(new_password) < 6:
                    st.markdown("""
                                        <div style="
                                            background: linear-gradient(135deg, rgba(255,180,0,0.2), rgba(255,140,0,0.1));
                                            border: 1px solid rgba(255,180,0,0.4);
                                            color: #ffe9c6;
                                            padding: 20px;
                                            border-radius: 16px;
                                            font-size: 15px;
                                            margin-top: 10px;
                                            width: 260%;
                                            box-shadow: 0 0 15px rgba(255,180,0,0.15);
                                        ">
                                        ⚠️ Şifre en az 6 karakter olmalı!
                                        </div>
                                        """, unsafe_allow_html=True)

                else:
                    user = get_user(username)

                    if not user:
                        st.markdown("""
                        <div style="
                            background: linear-gradient(135deg, rgba(255,0,0,0.15), rgba(255,0,0,0.05));
                            border: 1px solid rgba(255,0,0,0.4);
                            color: #ffd6d6;
                            padding: 20px;
                            border-radius: 16px;
                            font-size: 15px;
                            margin-top: 10px;
                            width: 240%;
                            margin: 10px auto;
                            box-shadow: 0 0 15px rgba(255,0,0,0.2);
                        ">
                        ❌ Kullanıcı bulunamadı. Bilgilerinizi kontrol edin.
                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        new_hashed = hash_password(new_password)
                        updated = update_password(username, new_hashed)

                        if not updated:
                            st.error("❌ Güncelleme başarısız!")

                        else:
                            st.success("Şifre güncellendi ✅")
                            st.session_state.page = "login"
                            st.rerun()

        with col_btn2:
            if st.button("Geri Dön", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()


# result
elif st.session_state.page == "result":
    show_app_header()
    st.title("📊 Sonuçlar")

    if st.session_state.password_result is None or st.session_state.habits_score is None:
        st.error("Sonuç bilgisi bulunamadı.")

        if st.button("Ana Menüye Dön"):
            st.session_state.page = "login"
            reset_user_flow()
            st.rerun()

    else:
        password_score = st.session_state.password_result["score"]
        habits_score = st.session_state.habits_score

        score_result = ScoreResult()
        total = score_result.calculateTotal(password_score, habits_score)
        category = score_result.getCategory()

        st.metric("Toplam Skor", total)
        st.write(f"**Seviye:** {category}")
        st.write(f"**Risk:** {st.session_state.risk}")

        if total < 40:
            total_color = "#EF4444"  # Kırmızı
        elif total < 80:
            total_color = "#F59E0B"  # Turuncu
        else:
            total_color = "#10B981"  # Yeşil

        st.write("📅 Tarih:", datetime.now().strftime("%d.%m.%Y %H:%M"))
        st.subheader("📈 Skor Dağılımı")

        col1, col2, col3 = st.columns(3)

        scores = [
            ("Şifre Skoru", (password_score / 5) * 100, "#3B82F6"),
            ("Alışkanlık Skoru", (habits_score / 12) * 100, "#10B981"),
            ("Toplam Skor", total, total_color)
        ]

        for col, (title, value, color) in zip([col1, col2, col3], scores):
            with col:
                fig = px.pie(
                    values=[value, 100 - value],
                    names=[title, ""],
                    hole=0.75
                )

                fig.update_traces(
                    marker=dict(colors=[color, "#1F2937"]),
                    textinfo="none"
                )

                fig.update_layout(
                    annotations=[
                        dict(
                            text=f"<b>%{value:.0f}</b>",
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font_size=24,
                            font_color="white"
                        )
                    ],
                    showlegend=False,
                    height=250,
                    margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117",
                    font_color="white",
                    title=title
                )

                st.plotly_chart(fig, use_container_width=True)

        if not st.session_state.result_saved:
            save_result(
                st.session_state.user_id,
                password_score,
                habits_score,
                total,
                category
            )
            st.session_state.result_saved = True

        feedback = feedback_service.generateFeedback(total)
        st.info(feedback)

        st.markdown("**Şifre Geri Bildirimleri:**")
        for fb in st.session_state.password_result["feedback"]:
            st.warning(fb)

        st.markdown("""
        ### 🎓 Siber Güvenlik Farkındalığını Artırın

        Siber güvenlik bilincinizi geliştirmek, güncel tehditler hakkında bilgi edinmek ve daha güvenli dijital alışkanlıklar kazanmak için aşağıdaki kaynakları inceleyebilirsiniz.
        """)

        st.link_button(
            "📚 BTK Akademi Siber Güvenlik Eğitimleri",
            "https://www.btkakademi.gov.tr"
        )

        st.link_button(
            "🛡️ USOM Siber Güvenlik Farkındalık Rehberleri",
            "https://www.usom.gov.tr"
        )

        if st.button("Çıkış Yap"):
            st.session_state.clear()
            st.session_state.page = "login"
            reset_user_flow()
            st.rerun()


# admin panel
elif st.session_state.page == "admin":
    show_app_header()
    st.title("📊 Admin Panel")

    if st.session_state.role != "admin":
        st.error("Bu sayfaya erişim yetkiniz yok.")

        if st.button("Girişe Dön"):
            st.session_state.page = "login"
            st.rerun()
    else:
        results = get_all_results()

        if results:
            df = pd.DataFrame(results, columns=[
                "username",
                "age_group",
                "education_level",
                "occupation",
                "password",
                "habits",
                "total",
                "category",
                "date"
            ])
            df["password_percent"] = (df["password"] / 5) * 100
            df["habits_percent"] = (df["habits"] / 12) * 100

            st.subheader("📋 Tüm Kullanıcı Sonuçları")
            st.dataframe(df, use_container_width=True)

            # istatistikler
            st.subheader("📊 Genel İstatistikler")

            avg_score = df["total"].mean()
            max_score = df["total"].max()
            min_score = df["total"].min()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Ortalama Skor", round(avg_score, 2))
            col2.metric("En Yüksek", max_score)
            col3.metric("En Düşük", min_score)
            col4.metric("Toplam Kullanıcı", len(df))

            # dağılım
            st.subheader("📈 Seviye Dağılımı")

            distribution = df["category"].value_counts().reset_index()
            distribution.columns = ["Seviye", "Kullanıcı Sayısı"]

            colors = {
                "Zayıf": "#1565C0",  # Koyu mavi
                "Orta": "#64B5F6",  # Açık mavi
                "Güçlü": "#90CAF9"  # Çok açık mavi
            }

            col1, col2 = st.columns(2)

            with col1:
                fig_bar = px.bar(
                    distribution,
                    x="Seviye",
                    y="Kullanıcı Sayısı",
                    color="Seviye",
                    text="Kullanıcı Sayısı",
                    title="Farkındalık Seviyesi Dağılımı",
                    color_discrete_map=colors
                )

                fig_bar.update_layout(
                    showlegend=False,
                    xaxis_title="Seviye",
                    yaxis_title="Kullanıcı Sayısı",
                    plot_bgcolor="#0E1117",
                    paper_bgcolor="#0E1117",
                    font_color="white"
                )

                st.plotly_chart(fig_bar, use_container_width=True)

            with col2:
                fig_pie = px.pie(
                    distribution,
                    values="Kullanıcı Sayısı",
                    names="Seviye",
                    title="Seviye Oranları",
                    hole=0.4,
                    color="Seviye",
                    color_discrete_map=colors
                )

                fig_pie.update_layout(
                    plot_bgcolor="#0E1117",
                    paper_bgcolor="#0E1117",
                    font_color="white"
                )

                st.plotly_chart(fig_pie, use_container_width=True)

            # zaman grafiği
            st.subheader("📅 Zaman Bazlı Skorlar")

            df["date"] = pd.to_datetime(df["date"])
            df_sorted = df.sort_values("date")

            st.line_chart(df_sorted.set_index("date")["total"])

            #demografik analizler 
            st.markdown("---")
            st.subheader("📊 Demografik Analizler")

            # YAŞ
            st.markdown("### 👥 Yaş Gruplarına Göre Ortalama Toplam Farkındalık Skoru")

            age_analysis = df.groupby("age_group")["total"].mean().reset_index()

            fig_age = px.bar(
                age_analysis,
                x="age_group",
                y="total",
                text="total",
                title="Yaş Grupları Ortalama Skor",
                color_discrete_sequence=["#6C63FF"]
            )

            fig_age.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )
            fig_age.update_layout(
                xaxis_title="Yaş Grubu",
                yaxis_title="Ortalama Farkındalık Skoru (%)"
            )

            fig_age.update_yaxes(range=[0, 100])

            st.plotly_chart(fig_age, use_container_width=True)

            #eğitim
            st.markdown("### 🎓 Eğitim Durumuna Göre Ortalama Toplam Farkındalık Skoru")

            education_analysis = df.groupby("education_level")["total"].mean().reset_index()

            fig_education = px.bar(
                education_analysis,
                x="education_level",
                y="total",
                text="total",
                title="Eğitim Durumu Ortalama Skor",
                color_discrete_sequence=["#7C5CFC"]
            )

            fig_education.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )
            fig_education.update_layout(
                xaxis_title="Eğitim Durumu",
                yaxis_title="Ortalama Farkındalık Skoru (%)"
            )
            fig_education.update_yaxes(range=[0, 100])

            st.plotly_chart(fig_education, use_container_width=True)

            #meslek
            st.markdown("### 💼 Meslek Gruplarına Göre Ortalama Toplam Farkındalık Skoru")

            occupation_analysis = df.groupby("occupation")["total"].mean().reset_index()

            fig_occupation = px.bar(
                occupation_analysis,
                x="occupation",
                y="total",
                text="total",
                title="Meslek Grupları Ortalama Skor",
                color_discrete_sequence=["#8B5CF6"]
            )

            fig_occupation.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )

            fig_occupation.update_layout(
                xaxis_title="Meslek Grubu",
                yaxis_title="Ortalama Farkındalık Skoru (%)"
            )

            fig_occupation.update_yaxes(range=[0, 100])


            st.plotly_chart(fig_occupation, use_container_width=True)
            
            #detaylı analizler

            st.markdown("---")
            st.subheader("🔍 Detaylı Analizler")
            st.info(
                "Bu bölümde yaş grubu, eğitim durumu ve meslek gruplarına göre şifre güvenliği ve güvenli internet alışkanlıkları karşılaştırmalı olarak analiz edilmektedir."
            )

            # ŞİFRE SKORU
            st.markdown("### 🔐 Yaş Gruplarına Göre Ortalama Şifre Skoru")

            age_password = df.groupby("age_group")["password_percent"].mean().reset_index()

            fig_age_password = px.bar(
                age_password,
                x="age_group",
                y="password_percent",
                text="password_percent",
                title="Yaş Grupları Ortalama Şifre Skoru",
                color_discrete_sequence=["#00C2FF"]
            )

            fig_age_password.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )

            fig_age_password.update_layout(
                xaxis_title="Yaş Grubu",
                yaxis_title="Ortalama Şifre Skoru (%)"
            )

            fig_age_password.update_yaxes(range=[0, 100])
            st.plotly_chart(fig_age_password, use_container_width=True)

            # ALIŞKANLIK SKORU
            st.markdown("### 🌐 Yaş Gruplarına Göre Ortalama Alışkanlık Skoru")

            age_habits = df.groupby("age_group")["habits_percent"].mean().reset_index()

            fig_age_habits = px.bar(
                age_habits,
                x="age_group",
                y="habits_percent",
                text="habits_percent",
                title="Yaş Grupları Ortalama Alışkanlık Skoru",
                color_discrete_sequence=["#10B981"]
            )

            fig_age_habits.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )

            fig_age_habits.update_layout(
                xaxis_title="Yaş Grubu",
                yaxis_title="Ortalama Alışkanlık Skoru (%)"
            )

            fig_age_habits.update_yaxes(range=[0, 100])

            st.plotly_chart(fig_age_habits, use_container_width=True)

            # EĞİTİM DURUMUNA GÖRE ŞİFRE SKORU
            st.markdown("### 🎓 Eğitim Durumuna Göre Ortalama Şifre Skoru")

            education_password = df.groupby("education_level")["password_percent"].mean().reset_index()

            fig_education_password = px.bar(
                education_password,
                x="education_level",
                y="password_percent",
                text="password_percent",
                title="Eğitim Durumu Ortalama Şifre Skoru",
                color_discrete_sequence=["#3B82F6"]
            )

            fig_education_password.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )

            fig_education_password.update_layout(
                xaxis_title="Eğitim Durumu",
                yaxis_title="Ortalama Şifre Skoru (%)"
            )

            fig_education_password.update_yaxes(range=[0, 100])

            st.plotly_chart(fig_education_password, use_container_width=True)

            # EĞİTİM DURUMUNA GÖRE ALIŞKANLIK SKORU
            st.markdown("### 🌐 Eğitim Durumuna Göre Ortalama Alışkanlık Skoru")

            education_habits = df.groupby("education_level")["habits_percent"].mean().reset_index()

            fig_education_habits = px.bar(
                education_habits,
                x="education_level",
                y="habits_percent",
                text="habits_percent",
                title="Eğitim Durumu Ortalama Alışkanlık Skoru",
                color_discrete_sequence=["#14B8A6"]
            )

            fig_education_habits.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )

            fig_education_habits.update_layout(
                xaxis_title="Eğitim Durumu",
                yaxis_title="Ortalama Alışkanlık Skoru (%)"
            )

            fig_education_habits.update_yaxes(range=[0, 100])

            st.plotly_chart(fig_education_habits, use_container_width=True)

            # MESLEK GRUBUNA GÖRE ŞİFRE SKORU
            st.markdown("### 💼 Meslek Gruplarına Göre Ortalama Şifre Skoru")

            occupation_password = df.groupby("occupation")["password_percent"].mean().reset_index()

            fig_occupation_password = px.bar(
                occupation_password,
                x="occupation",
                y="password_percent",
                text="password_percent",
                title="Meslek Grupları Ortalama Şifre Skoru",
                color_discrete_sequence=["#6366F1"]
            )

            fig_occupation_password.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )

            fig_occupation_password.update_layout(
                xaxis_title="Meslek Grubu",
                yaxis_title="Ortalama Şifre Skoru (%)"
            )

            fig_occupation_password.update_yaxes(range=[0, 100])

            st.plotly_chart(fig_occupation_password, use_container_width=True)

            # MESLEK GRUBUNA GÖRE ALIŞKANLIK SKORU
            st.markdown("### 🌍 Meslek Gruplarına Göre Ortalama Alışkanlık Skoru")

            occupation_habits = df.groupby("occupation")["habits_percent"].mean().reset_index()

            fig_occupation_habits = px.bar(
                occupation_habits,
                x="occupation",
                y="habits_percent",
                text="habits_percent",
                title="Meslek Grupları Ortalama Alışkanlık Skoru",
                color_discrete_sequence=["#10B981"]
            )

            fig_occupation_habits.update_traces(
                texttemplate='%{y:.1f}',
                textposition='outside'
            )

            fig_occupation_habits.update_layout(
                xaxis_title="Meslek Grubu",
                yaxis_title="Ortalama Alışkanlık Skoru (%)"
            )

            fig_occupation_habits.update_yaxes(range=[0, 100])

            st.plotly_chart(fig_occupation_habits, use_container_width=True)

        else:
            st.warning("Henüz veri yok")

        if st.button("Çıkış"):
            st.session_state.page = "login"
            st.session_state.user_id = None
            st.session_state.username = ""
            st.session_state.role = ""
            reset_user_flow()
            st.rerun()