ENVIRONMENT=dev

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log

copy-ssh-keys:
	mkdir -p ./.keys/
	cp -r ~/.ssh/* ./.keys/

build: copy-ssh-keys

bash: copy-ssh-keys