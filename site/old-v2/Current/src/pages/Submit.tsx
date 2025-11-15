import { useEffect } from "react";

const Submit = () => {
  useEffect(() => {
    // Dynamically load the Fillout embed script
    const script = document.createElement("script");
    script.src = "https://server.fillout.com/embed/v1/";
    script.async = true;
    document.body.appendChild(script);

    // Cleanup on unmount
    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0 }}>
      <div
        data-fillout-id="cAEHXgvZhWus"
        data-fillout-embed-type="fullscreen"
        style={{ width: "100%", height: "100%" }}
        data-fillout-inherit-parameters
        data-fillout-domain="forms.hackclub.com"
      ></div>
    </div>
  );
};

export default Submit;