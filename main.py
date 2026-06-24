import hashlib
import re
from db import register, login, save_result, get_results

class PasswordTest:

    def __init__(self):
        self.questions = [
            "En az 8 karakter var mı?",
            "Büyük harf içeriyor mu?",
            "Küçük harf içeriyor mu?",
            "Rakam içeriyor mu?",
            "Özel karakter içeriyor mu?"
        ]
        self.max_score = 5

    def getQuestions(self):
        return self.questions

    def evaluate(self, password):
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Parola en az 8 karakter olmalıdır.")

        if re.search(r"[A-Z]", password):
            score += 1
        else:
            feedback.append("Büyük harf ekleyin.")

        if re.search(r"[a-z]", password):
            score += 1
        else:
            feedback.append("Küçük harf ekleyin.")

        if re.search(r"[0-9]", password):
            score += 1
        else:
            feedback.append("Rakam ekleyin.")

        if re.search(r"[!@#$%^&*]", password):
            score += 1
        else:
            feedback.append("Özel karakter ekleyin.")

        level = self.analyzeStrength(score)

        return {
            "score": score,
            "level": level,
            "feedback": feedback
        }

    def analyzeStrength(self, score):
        if score <= 2:
            return "Zayıf"
        elif score <= 4:
            return "Orta"
        else:
            return "Güçlü"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Habits test
class HabitsTest:

    def __init__(self):
        self.questions = [
            ("Bilinmeyen linklere tıklar mısınız?", "h",
             "Link: Bir web sayfasına veya dosyaya yönlendiren bağlantıdır."),

            ("Aynı şifreyi birden fazla yerde kullanır mısınız?", "h",
             "Aynı parolanın birden fazla hesapta kullanılması güvenlik riskini artırır."),

            ("Antivirüs kullanıyor musunuz?", "e",
             "Antivirüs: Virüsleri ve zararlı yazılımları tespit edip engelleyen güvenlik yazılımıdır."),

            ("Şifrelerinizi düzenli değiştirir misiniz?", "e",
             "Parolaların belirli aralıklarla değiştirilmesi hesap güvenliğini artırabilir."),

            ("İki faktörlü doğrulama (2FA) kullanır mısınız?", "e",
             "2FA: Şifreye ek olarak SMS, e-posta veya uygulama kodu ile ikinci doğrulama yapılmasıdır."),

            ("Halka açık Wi-Fi'de hassas işlem yapar mısınız?", "h",
             "Halka açık Wi-Fi: Herkesin bağlanabildiği ortak kablosuz internet ağıdır."),

            ("E-posta eklerini kontrol etmeden açar mısınız?", "h",
             "E-posta ekleri zararlı yazılım içerebilir, açmadan önce kontrol edilmelidir."),

            ("Güvenmediğiniz sitelere kişisel bilgi girer misiniz?", "h",
             "Kişisel bilgiler yalnızca güvenilir ve doğrulanmış sitelerde paylaşılmalıdır."),

            ("Yazılımlarınızı güncel tutar mısınız?", "e",
             "Yazılım güncellemeleri güvenlik açıklarını kapatabilir."),

            ("Tarayıcıda şifre kaydetme kullanır mısınız?", "h",
             "Tarayıcı: Chrome, Edge, Firefox gibi internete erişim sağlayan programlardır."),

            ("Kullandığınız hesaplarda farklı parolalar kullanır mısınız?", "e",
             "Her hesap için farklı parola kullanılması güvenliği artırır."),

            ("İşletim sistemi ve uygulama güncellemelerini geciktirmeden yükler misiniz?", "e",
             "İşletim sistemi: Bilgisayar, telefon veya tabletin çalışmasını sağlayan temel yazılımdır. Uygulamaların açılması, dosyaların yönetilmesi ve cihazın kullanılabilmesi için gereklidir. Windows, Android ve macOS işletim sistemlerine örnek olarak verilebilir.")
        ]
        self.max_score = len(self.questions)

    def getQuestions(self):
        return self.questions

    def evaluate(self):
        score = 0

        print("\nGüvenli İnternet Alışkanlıkları Testi:")

        for i, (question, correct_answer, info) in enumerate(self.questions, start=1):
            answer = input(f"{i}. {question} (e/h): ").lower()

            if answer == correct_answer:
                score += 1

        return score

    def assessRisk(self, score):
        if score <= self.max_score * 0.3:
            return "Yüksek Risk"
        elif score <= self.max_score * 0.7:
            return "Orta Risk"
        else:
            return "Düşük Risk"

# score result
class ScoreResult:

    def __init__(self):
        self.password_score = 0
        self.habits_score = 0
        self.total_score = 0

    def calculateTotal(self, password_score, habits_score):
        self.password_score = password_score
        self.habits_score = habits_score

        # Şifre testi %50, alışkanlık testi %50 ağırlıklı
        self.total_score = ((password_score / 5) * 50) + ((habits_score / 12) * 50)

        return round(self.total_score)

    def getCategory(self):
        if self.total_score < 40:
            return "Zayıf"
        elif self.total_score < 80:
            return "Orta"
        else:
            return "Güçlü"

    def get_summary(self):
        return {
            "password_score": self.password_score,
            "habits_score": self.habits_score,
            "total_score": self.total_score,
            "category": self.getCategory()
        }

    def save(self):
        print(f"[KAYIT] Toplam Skor: {self.total_score} ({self.getCategory()})")

    def __str__(self):
        return f"Toplam Skor: {self.total_score} | Seviye: {self.getCategory()}"

# feedback service
class FeedbackService:

    def __init__(self):
        self.templates = {
            "low": "Güvenlik seviyeniz düşük olarak değerlendirilmiştir. Parola güvenliği ve dijital alışkanlıklarınız çeşitli riskler içermektedir. Daha güçlü parolalar kullanmanız, hesap güvenliği ayarlarınızı gözden geçirmeniz ve güvenli internet kullanım alışkanlıkları geliştirmeniz önerilmektedir.",

            "medium": "Güvenlik seviyeniz orta düzeydedir. Temel güvenlik önlemlerinin bir kısmını uyguluyor olsanız da geliştirilmesi gereken alanlar bulunmaktadır. Parola karmaşıklığını artırmanız, hesap güvenliği ayarlarınızı düzenli olarak kontrol etmeniz ve güvenli dijital davranışları sürdürmeniz tavsiye edilmektedir.",

            "high": "Güvenlik seviyeniz yüksek olarak değerlendirilmiştir. Parola güvenliği ve dijital farkındalık açısından güçlü bir profil sergilemektesiniz. Mevcut güvenlik alışkanlıklarınızı sürdürmeniz ve güncel siber tehditlere karşı farkındalığınızı korumanız önerilmektedir."
        }

    def getFeedbackText(self, level):
        return self.templates.get(level, "Geçersiz seviye.")

    def generateFeedback(self, score):
        if score < 40:
            return self.getFeedbackText("low")
        elif score < 80:
            return self.getFeedbackText("medium")
        else:
            return self.getFeedbackText("high")

#istatistisel analiz
class StatisticalAnalysis:

    def computeStats(self, results):
        if not results:
            return None

        total_scores = [r[3] for r in results]

        avg = sum(total_scores) / len(total_scores)
        max_score = max(total_scores)
        min_score = min(total_scores)

        return {
            "average": avg,
            "max": max_score,
            "min": min_score,
            "count": len(results)
        }

    def computeDistributions(self, results):
        if not results:
            return None

        distribution = {
            "Zayıf": 0,
            "Orta": 0,
            "Güçlü": 0
        }

        for r in results:
            category = r[4]
            if category in distribution:
                distribution[category] += 1

        return distribution

    def analyzeByDemographic(self, results):
        return {
            "message": "Demografik analiz için veri bulunmamaktadır."
        }

    def generateReport(self, stats):
        if not stats:
            print("Veri yok")
            return

        print("\n=== İSTATİSTİKSEL ANALİZ ===")
        print("Ortalama Skor:", round(stats["average"], 2))
        print("En Yüksek Skor:", stats["max"])
        print("En Düşük Skor:", stats["min"])
        print("Toplam Kullanım:", stats["count"])

class AuthenticationService:

    def authenticate(self, username, password):
        return login(username, password)

    def registerUser(self, username, email, password):
        return register(username, email, password)


class EvaluationSession:

    def __init__(self):
        self.auth = AuthenticationService()
        self.password_test = PasswordTest()
        self.habits_test = HabitsTest()
        self.feedback_service = FeedbackService()

    def start(self):

        print("Siber Güvenlik Farkındalık Analizi\n")
        print("Giriş Yap")

        # login
        username = input("Kullanıcı adı: ")
        login_password = input("Şifre: ")

        hashed_password = hash_password(login_password)
        user_id = self.auth.authenticate(username, hashed_password)


        is_new_user = False

        if user_id is None:
            is_new_user = True
            print("Kullanıcı bulunamadı, kayıt oluşturuluyor...")
            email = input("Email giriniz: ")

            new_password = input("Yeni şifre belirleyin: ")
            hashed_password = hash_password(new_password)

            self.auth.registerUser(username, email, hashed_password)
            user_id = self.auth.authenticate(username, hashed_password)

        # pasword test
        if is_new_user:
            print("\nŞifreniz analiz ediliyor...")
            test_password = new_password

        else:
            test_password = input("Değerlendirme için farklı bir şifre giriniz (boş bırakılırsa mevcut kullanılır): ")
            if test_password == "":
                test_password = login_password

        result = self.password_test.evaluate(test_password)
        if is_new_user:
            print("\n--- ŞİFRE ANALİZİ (KAYIT ŞİFRESİ) ---")
            print("Şifreniz analiz edildi.")
        else:
            print("\n--- ŞİFRE ANALİZİ ---")

        #print("Şifre Skoru:", result["score"] * 20)
        #print("Şifre Seviyesi:", result["level"])

        password_score = result["score"]
        password_level = result["level"]
        password_feedback = result["feedback"]

        # habits test
        habits_score = self.habits_test.evaluate()
        risk = self.habits_test.assessRisk(habits_score)

        # score
        score_result = ScoreResult()
        total_score = score_result.calculateTotal(password_score, habits_score)
        category = score_result.getCategory()

        # DB register
        save_result(user_id, password_score, habits_score, total_score, category)

        # feedback
        feedback = self.feedback_service.generateFeedback(total_score)

        score_result.save()

        # statistic
        results = get_results(user_id)
        analysis = StatisticalAnalysis()
        stats = analysis.computeStats(results)
        analysis.generateReport(stats)

        # outputs
        print("\n===== SONUÇLAR =====")
        print("Şifre Skoru:", password_score * 20)
        print("Şifre Seviyesi:", password_level)

        print("Alışkanlık Skoru:", habits_score * 10)
        print("Risk Seviyesi:", risk)

        print("Toplam Skor:", total_score)
        print("Genel Seviye:", category)

        print("\n--- Şifre Geri Bildirimleri ---")
        for fb in password_feedback:
            print("-", fb)

        print("\n--- Genel Geri Bildirim ---")
        print(feedback)


from db import create_database

if __name__ == "__main__":
    create_database()

    session = EvaluationSession()
    session.start()

    import sqlite3

    conn = sqlite3.connect("sgf_wu.db")
    cursor = conn.cursor()

    print("\n--- USERS TABLOSU ---")
    cursor.execute("SELECT * FROM users")
    for u in cursor.fetchall():
        print(u)

    print("\n--- SCORE RESULTS TABLOSU ---")
    cursor.execute("SELECT * FROM score_results")
    for r in cursor.fetchall():
        print(r)

    conn.close()