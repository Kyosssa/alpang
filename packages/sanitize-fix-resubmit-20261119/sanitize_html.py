#!/usr/bin/env python3
# sanitize_html.py — 소스 정화 단계 (2026-11-17 TL-017 CF 흔적 회귀 후 신설 · 2026-11-19 규칙 순서 정정)
# 라이브 수집본을 동결 기준본으로 쓸 때 Cloudflare가 변환한 흔적을 걷어낸다.
# 규칙 순서 (2026-11-19 판정 bbd4508 정정): 비콘 -> decode -> 이메일 링크 -> 주석 쌍.
#   주석 쌍 삭제가 비컨 삭제보다 먼저면, 비컨이 주석 사이에 낀 수집본에서 주석 쌍이 잔존해 실패한다.
#   1) 비콘 스크립트 (cloudflareinsights) 삭제
#   2) email-decode 스크립트 삭제
#   3) 푸터 문의 링크 href="/cdn-cgi/l/email-protection#..." -> href="mailto:alpangland@gmail.com"
#   4) </body> 앞 빈 주석 쌍 <!-- Cloudflare Pages Analytics --><!-- Cloudflare Pages Analytics --> 삭제
# 적용 후 cdn-cgi · Analytics 잔존이 0이 아니면 실패로 종료한다.
# 파일 입출력은 encoding='utf-8', newline='' 명시 (Windows CRLF · cp949 대응).
# 사용: python3 sanitize_html.py <file> [file...]  (제자리 정화 + 파일별 결과 출력)
# 파이프라인 위치: 라이브 수집본을 동결 기준본으로 채택하는 단계 직후, 기준본 확정 전에 적용한다.
import re, sys

def sanitize(html):
    html, n1 = re.subn(r'<script[^>]*cloudflareinsights[^>]*></script>', '', html)
    html, n2 = re.subn(r'<script[^>]*email-decode[^>]*></script>', '', html)
    html, n3 = re.subn(r'href="/cdn-cgi/l/email-protection#[^"]*"', 'href="mailto:alpangland@gmail.com"', html)
    html, n4 = re.subn(r'<!-- Cloudflare Pages Analytics --><!-- Cloudflare Pages Analytics -->', '', html)
    return html, (n1, n2, n3, n4)

if __name__ == '__main__':
    ok = True
    for path in sys.argv[1:]:
        raw = open(path, encoding='utf-8', newline='').read()
        out, counts = sanitize(raw)
        if 'cdn-cgi' in out or 'Analytics' in out:
            print(f'FAIL {path}: cdn-cgi/Analytics 잔존'); ok = False; continue
        if out != raw:
            open(path, 'w', encoding='utf-8', newline='').write(out)
        print(f'OK {path}: beacon {counts[0]} · email-decode {counts[1]} · email-protection {counts[2]} · analytics-pair {counts[3]} · delta {len(out.encode()) - len(raw.encode())}B')
    sys.exit(0 if ok else 1)
