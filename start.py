from rest import app
import config as cfg

if __name__ == "__main__":
    app.run(cfg.host, cfg.port, debug=False)