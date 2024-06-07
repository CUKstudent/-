import pandas as pd

# 레벤슈타인 거리 계산 함수
def calc_distance(a, b):
    ''' 레벤슈타인 거리 계산하기 '''
    if a == b:
        return 0
    a_len = len(a)
    b_len = len(b)
    if a == "":
        return b_len
    if b == "":
        return a_len
    
    matrix = [[0] * (b_len + 1) for _ in range(a_len + 1)]
    for i in range(a_len + 1):
        matrix[i][0] = i
    for j in range(b_len + 1):
        matrix[0][j] = j

    for i in range(1, a_len + 1):
        for j in range(1, b_len + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,  # 문자 제거
                matrix[i][j - 1] + 1,  # 문자 삽입
                matrix[i - 1][j - 1] + cost  # 문자 변경
            )
    return matrix[a_len][b_len]

# 챗봇 클래스를 정의
class LevenshteinChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers

    def find_best_answer(self, input_sentence):
        distances = [calc_distance(input_sentence, question) for question in self.questions]
        best_match_index = distances.index(min(distances))
        return self.answers[best_match_index]

# 데이터 파일의 경로를 지정합니다.
filepath = 'ChatbotData.csv'

# 챗봇 객체를 생성합니다.
chatbot = LevenshteinChatBot(filepath)

# '종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)