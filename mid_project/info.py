한국 음원 audio_feature사이트: TuneBat

# 카멜롯, 키 중 카멜롯 사용하는게 좋을듯(좀더 사람이 듣는 분위기랑 더 비슷)
 # 카멜롯 인코딩방법: Embedding 또는 Sine/Cosine 인코딩 (권장)
원형 데이터를 숫자로 인코딩할 때는 sin/cos 변환이 최적입니다.

import numpy as np

camelot_number = 8   # 1~12
angle = 2 * np.pi * (camelot_number - 1) / 12
camelot_sin = np.sin(angle)
camelot_cos = np.cos(angle)

결과:
camelot_sin ≈ 0.866
camelot_cos ≈ -0.5
➡️ 최종 피쳐 벡터: [camelot_sin, camelot_cos, camelot_mode] (3차원)

장점:

1A와 12A가 가깝다는 걸 수학적으로 표현 가능

원형 구조를 유지한 채 숫자 인코딩 가능

많은 실제 모델에서 사용되는 방식 (시간, 각도 등에서)
