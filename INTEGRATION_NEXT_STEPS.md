# Integration Next Steps for annuitynest.com/custom-quote/

This document outlines the recommended next steps to integrate the running app into https://annuitynest.com/custom-quote/.

## 1) Choose Integration Approach

Pick one of these based on desired UX and maintenance:

- **Iframe embed (fastest, least invasive)**
  - Use the existing auto-resize postMessage flow already implemented in `static/script.js`.
  - Pros: minimal WordPress changes, no plugin build.
  - Cons: iframe UX constraints, analytics/tracking coordination needed.

- **WordPress native embed (Elementor HTML widget + API calls)**
  - Build the form in Elementor and call the Flask API endpoint directly.
  - Pros: native look and feel, no iframe.
  - Cons: more frontend work, CORS setup required.

- **WordPress plugin (longer-term)**
  - Package the form and API proxy into a plugin.
  - Pros: maintainability, security controls, easy updates.
  - Cons: higher effort and timeline.

Recommendation for now: **Iframe embed** to validate production traffic, then migrate to a native embed or plugin if needed.

## 2) Production Domain and SSL

- Assign a production subdomain for the Flask app (e.g., `quote.annuitynest.com`).
- Update DNS to point to the Coolify instance.
- Enable SSL for the subdomain in Coolify.
- Keep the current deployment as staging:
  - Current URL: http://xwg000gwogws8ook004cs0g4.46.224.23.170.sslip.io/

## 3) Embed on the WordPress Page

Add this to a Custom HTML block on https://annuitynest.com/custom-quote/ (update the domain):

```html
<div class="annuity-calculator-wrapper">
  <iframe 
    id="annuity-calculator"
    src="https://quote.annuitynest.com" 
    width="100%" 
    height="900" 
    frameborder="0"
    scrolling="no"
    style="border: none;">
  </iframe>
</div>

<script>
  // Auto-resize iframe based on content height
  window.addEventListener('message', function(e) {
    if (e.origin !== 'https://quote.annuitynest.com') return;
    if (e.data.type === 'resize') {
      document.getElementById('annuity-calculator').style.height = e.data.height + 'px';
    }
  });
</script>
```

## 4) CORS / CSP Considerations

- If using iframe, ensure the Flask app allows being embedded:
  - Set appropriate `X-Frame-Options` (do not set `DENY`).
  - Add/adjust a `Content-Security-Policy` `frame-ancestors` directive to allow `annuitynest.com`.
- If using direct API calls from the WordPress page, configure CORS to allow `https://annuitynest.com`.

## 5) Lead Capture and CRM Routing

Decide where submissions should land:

- Email notification
- CRM (e.g., HubSpot, Salesforce, etc.)
- Database storage

If required, add a webhook call in `app.py` to forward completed submissions to the CRM or email service.

## 6) Analytics and Conversion Tracking

- Ensure the WordPress page can track successful quote submissions.
- If iframe-based, consider sending a `postMessage` event from the app to the parent page for conversion tracking.

## 7) Hardening and Monitoring

- Add rate limiting for `/api/calculate`.
- Add logging for errors and request metrics.
- Set up uptime monitoring for `/health`.
- Confirm backups for the Excel files.

## 8) Final QA Checklist

- Verify the page looks correct in Elementor and mobile.
- Test with multiple states and investment amounts.
- Validate both Fixed and Variable flows.
- Confirm iframe resizes correctly when results appear.
- Confirm form submission works under HTTPS.

---

If you want, I can also:
- add an environment-based `ALLOWED_ORIGINS` config for CORS
- add a `frame-ancestors` CSP header
- add a webhook for lead delivery
