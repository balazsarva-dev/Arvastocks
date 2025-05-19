import React from "react";
import "../stocks/Chart.css";

const Donation = () => (
  <div className="chart-container donation-center">
    <h1 className="chart-title">Donation</h1>
    <p className="chart-description">
      If you find our app useful and would like to support its development, consider making a donation. Your contributions help us maintain and improve the app.
    </p>
    <form
      action="https://www.paypal.com/donate"
      method="post"
      target="_blank"
      style={{ marginTop: 24, marginBottom: 24 }}
    >
      <input type="hidden" name="hosted_button_id" value="3PK38NH9UYM4A" />
      <input
        type="image"
        src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif"
        border="0"
        name="submit"
        title="PayPal - The safer, easier way to pay online!"
        alt="Donate with PayPal button"
      />
      <img
        alt=""
        border="0"
        src="https://www.paypal.com/en_HU/i/scr/pixel.gif"
        width="1"
        height="1"
        style={{ display: "none" }}
      />
    </form>
    <p className="chart-description">Thank you for your support!</p>
  </div>
);

export default Donation;