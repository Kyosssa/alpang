#!/usr/bin/env python3
# sanitize_html.py — 소스 정화 단계 (2026-11-17 TL-017 CF 흔적 회귀 후 신설)
# 라이브 수집본을 동결 기준본으로 쓸 때 Cloudflare가 변환한 흔적을 걷어낸다.
# 규칙:
#   1) 푸터 문의 링크 href="/cdn-cgi/l/email-protection#..." -> href="mailto:alpangland@gmail.com"
#   2) </body> 앞 빈 주석 쌍 <!-- Cloudflare Pages Analytics --><!-- Cloudflare Pages Analytics --> 삭제
#   3) 비콘 스크립트 (cloudflareinsights) · email-decode 스크립트 삭제
# 적용 후 cdn-cgi · Analytics 잔존이 0이 아니면 실패로 종료한다.
# 사용: python3 sanitize_html.py <file> [file...]  (제자리 정화 + 파일별 결과 출력)
import re, sys

def sanitize(html):
    html, n1 = re.subn(r'href="/cdn-cgi/l/email-protection#[^"]*"', 'href="mailto:alpangland@gmail.com"', html)
    html, n2 = re.subn(r'<!-- Cloudflare Pages Analytics --><!-- Cloudflare Pages Analytics -->', '', html)
    html, n3 = re.subn(r'<script[^>]*cloudflareinsights[^>]*></script>', '', html)
    html, n4 = re.subn(r'<script[^>]*email-decode[^>]*></script>', '', html)
    return html, (n1, n2, n3, n4)

if __name__ == '__main__':
    ok = True
    for path in sys.argv[1:]:
        raw = open(path).read()
        out, counts = sanitize(raw)
        if 'cdn-cgi' in out or 'Analytics' in out:
            print(f'FAIL {path}: cdn-cgi/Analytics 잔존'); ok = False; continue
        if out != raw:
            open(path, 'w').write(out)
        print(f'OK {path}: email-protection {counts[0]} · analytics-pair {counts[1]} · beacon {counts[2]} · email-decode {counts[3]} · delta {len(out.encode()) - len(raw.encode())}B')
    sys.exit(0 if ok else 1)
