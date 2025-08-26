# omojumiller.com

A python pelican personal blog deployed using Github pages

## License

The contents of this repository are covered under the [GNU GENERAL PUBLIC LICENSE](License.md).

## Install
```bash
python3 -m venv new_pelican_env
source new_pelican_env/bin/activate
pip install -r requirements.txt
make html    
make devserver PORT=8000  # dev local build
make publish # production build
```