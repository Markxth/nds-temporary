import pycurl
from io import BytesIO 
import certifi 
import ollama 

def read_input(filename) : 
    with open(filename, "r") as f:
       return f.read().strip() #strip is for removing the newline at the end of the file
    
def main() : 
    try :
        buffer = BytesIO()
        website = "https://en.wikipedia.org/wiki/Mark_Antony" #complete with web link
        c = pycurl.Curl() 
        c.setopt(c.URL, website)
        c.setopt(c.FOLLOWLOCATION, True) #follow redirects like a browser would ; good for errors
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close() 
    except pycurl.error as e  : 
        print("error " ,e )

    #now that we performed a curl , we have infom in bytes

    body = buffer.getvalue() #fetch info
    body = body.decode("utf-8") #make it readable
    print(body)

    #pass to LLM
    body_limit = body[:1500] #llama 3.2 limit is 2048 token, being ~1500 words
    response = ollama.generate(model='llama3.2', prompt=f'Summarise this website : {body_limit}')
    print(response['response']) #print output


if __name__ == "__main__" :
    main()