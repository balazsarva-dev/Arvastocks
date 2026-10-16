import { Link } from 'react-router-dom';

// PayPal redirects back to /donation-success, which renders this page with `thanks`.
export default function Donate({ thanks = false }) {
  if (thanks) {
    return (
      <article className="prose center">
        <h1>Thank you for your donation!</h1>
        <p>Your support helps with the further development and maintenance of this project.</p>
        <Link to="/" className="button">Back to Markets</Link>
      </article>
    );
  }

  return (
    <article className="prose center">
      <h1>Support Arvastocks</h1>
      <p>
        If you find the app useful and would like to support its development, consider making a
        donation. Your contribution helps keep it running and improving.
      </p>
      <form action="https://www.paypal.com/donate" method="post" target="_blank">
        <input type="hidden" name="hosted_button_id" value="3PK38NH9UYM4A" />
        <button type="submit" className="button">Donate with PayPal</button>
      </form>
    </article>
  );
}
