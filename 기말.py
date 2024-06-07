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
        data = pd.read_csv(filepath) # CSV파일 읽어오기(DataFram 형태)
        questions = data['Q'].tolist() # 질문들을 리스트로 변환
        answers = data['A'].tolist() # 응답들을 리스트로 변환
        return questions, answers

    def find_best_answer(self, input_sentence):
        distances = [calc_distance(input_sentence, question) for question in self.questions] # 학습데이터와 chat의 질문의 유사도를 계산해 distances리스트에 저장
        best_match_index = distances.index(min(distances)) # 가장 작은 유사도의 인덱스 추출
        return self.answers[best_match_index] # 인덱스에 해당하는 응답 반환

# 데이터 파일의 경로를 지정
filepath = 'ChatbotData.csv'

# 챗봇 객체를 생성
chatbot = LevenshteinChatBot(filepath)

# '종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)