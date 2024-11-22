from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def compare_specs(spec1, spec2):
    try:
        # GPT API를 사용하여 기술 스펙 비교
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "두 기업의 기술 스펙을 비교하여 일치율을 분석해주세요. 백분율로 표시하고, 주요 차이점도 설명해주세요."},
                {"role": "user", "content": f"기업 A의 기술 스펙:\n{spec1}\n\n기업 B의 기술 스펙:\n{spec2}"}
            ],
            temperature=0.5
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

# HTML 템플릿
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>기술 스펙 비교 분석</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            textarea {
                width: 100%;
                min-height: 150px;
                margin: 10px 0;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            button {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            #result {
                margin-top: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>기술 스펙 비교 분석</h1>
            <div>
                <h3>기업 A의 기술 스펙:</h3>
                <textarea id="spec1" placeholder="기업 A의 기술 스펙을 입력하세요..."></textarea>
            </div>
            <div>
                <h3>기업 B의 기술 스펙:</h3>
                <textarea id="spec2" placeholder="기업 B의 기술 스펙을 입력하세요..."></textarea>
            </div>
            <button onclick="compareSpecs()">비교 분석</button>
            <div id="result"></div>
        </div>

        <script>
        async function compareSpecs() {
            const spec1 = document.getElementById('spec1').value;
            const spec2 = document.getElementById('spec2').value;
            
            if (!spec1 || !spec2) {
                alert('두 기업의 기술 스펙을 모두 입력해주세요.');
                return;
            }

            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '분석 중...';

            try {
                const response = await fetch('/compare', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ spec1, spec2 }),
                });
                
                const data = await response.json();
                resultDiv.innerHTML = data.result.replace(/\n/g, '<br>');
            } catch (error) {
                resultDiv.innerHTML = '오류가 발생했습니다: ' + error.message;
            }
        }
        </script>
    </body>
    </html>
    '''

@app.route('/compare', methods=['POST'])
def compare():
    data = request.json
    result = compare_specs(data['spec1'], data['spec2'])
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
