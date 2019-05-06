#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''
Created on 5 sept. 2016

@author: SL
'''

import re
from collections import Counter
from tme1.porter import stem
#from utils.porter import porter



class TextRepresenter(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def getTextRepresentation(self,text):
        raise NotImplementedError
    


class PorterStemmer(TextRepresenter):
    
    def __init__(self):
        '''
        Constructor
        '''
        self.stopWords=set()
        self._setStopWords()
        
    def getTextRepresentation(self,text, lower=True , stemm=True , stopwords=True  ):
        tab=re.findall(r"\w+",text,re.UNICODE)
        
        #print("s ",stopwords)
        res = []
        for word in tab : 
            if ( lower ) :
                word = word.lower()
            if ( stemm ) : 
                word = stem(word)
            if (( not stopwords ) or ( stopwords and word not in self.stopWords )) :
                res.append (word)
        
        return dict(Counter(res))
        


    def getQueryRepresentation(self , text , indexer  ):
        inverted_index = indexer.getInvertedIndex()
        tab=re.findall(r"\w+",text,re.UNICODE)
        res = []
        for word in tab : 
            if ( indexer.lower ) :
                word = word.lower()
            if ( indexer.stemm ) : 
                word = stem(word)
            if( (( not indexer.stopwords ) or 
                 ( indexer.stopwords and word not in self.stopWords ))
                and (word in inverted_index)   ) : 
                res.append (word)
        return res
    
    def getTermRepresentation ( self , term_tmp ,  lower=True ,
                               stemm=True , stopwords=True  ):
        
        if ( lower ) :
            term_tmp = term_tmp.lower()
        if ( stemm ) : 
            term_tmp = stem(term_tmp)
        if (( not stopwords ) or ( stopwords and term_tmp not in self.stopWords )) :
            return (term_tmp)
        else :
            return -1
        
            
        
        
        
    def _setStopWords(self):
        self.stopWords.add("a");
        self.stopWords.add("able");
        self.stopWords.add("about");
        self.stopWords.add("above");
        self.stopWords.add("according");
        self.stopWords.add("accordingly");
        self.stopWords.add("across");
        self.stopWords.add("actually");
        self.stopWords.add("after");
        self.stopWords.add("afterwards");
        self.stopWords.add("again");
        self.stopWords.add("against");
        self.stopWords.add("ain");
        self.stopWords.add("all");
        self.stopWords.add("almost");
        self.stopWords.add("alone");
        self.stopWords.add("along");
        self.stopWords.add("already");
        self.stopWords.add("also");
        self.stopWords.add("although");
        self.stopWords.add("always");
        self.stopWords.add("am");
        self.stopWords.add("among");
        self.stopWords.add("amongst");
        self.stopWords.add("amoungst");
        self.stopWords.add("an");
        self.stopWords.add("and");
        self.stopWords.add("another");
        self.stopWords.add("any");
        self.stopWords.add("anybody");
        self.stopWords.add("anyhow");
        self.stopWords.add("anyone");
        self.stopWords.add("anything");
        self.stopWords.add("anyway");
        self.stopWords.add("anyways");
        self.stopWords.add("anywhere");
        self.stopWords.add("ap");
        self.stopWords.add("apart");
        self.stopWords.add("are");
        self.stopWords.add("aren");
        self.stopWords.add("around");
        self.stopWords.add("as");
        self.stopWords.add("aside");
        self.stopWords.add("at");
        self.stopWords.add("available");
        self.stopWords.add("away");
        self.stopWords.add("awfully");
        self.stopWords.add("b");
        self.stopWords.add("back");
        self.stopWords.add("be");
        self.stopWords.add("because");
        self.stopWords.add("been");
        self.stopWords.add("before");
        self.stopWords.add("beforehand");
        self.stopWords.add("behind");
        self.stopWords.add("being");
        self.stopWords.add("below");
        self.stopWords.add("beside");
        self.stopWords.add("besides");
        self.stopWords.add("best");
        self.stopWords.add("better");
        self.stopWords.add("between");
        self.stopWords.add("beyond");
        self.stopWords.add("both");
        self.stopWords.add("bottom");
        self.stopWords.add("brief");
        self.stopWords.add("but");
        self.stopWords.add("by");
        self.stopWords.add("c");
        self.stopWords.add("came");
        self.stopWords.add("can");
        self.stopWords.add("cannot");
        self.stopWords.add("cant");
        self.stopWords.add("certain");
        self.stopWords.add("certainly");
        self.stopWords.add("clearly");
        self.stopWords.add("co");
        self.stopWords.add("com");
        self.stopWords.add("come");
        self.stopWords.add("comes");
        self.stopWords.add("con");
        self.stopWords.add("concerning");
        self.stopWords.add("consequently");
        self.stopWords.add("could");
        self.stopWords.add("couldn");
        self.stopWords.add("couldnt");
        self.stopWords.add("course");
        self.stopWords.add("currently");
        self.stopWords.add("d");
        self.stopWords.add("de");
        self.stopWords.add("definitely");
        self.stopWords.add("despite");
        self.stopWords.add("did");
        self.stopWords.add("didn");
        self.stopWords.add("different");
        self.stopWords.add("do");
        self.stopWords.add("does");
        self.stopWords.add("doesn");
        self.stopWords.add("doing");
        self.stopWords.add("don");
        self.stopWords.add("done");
        self.stopWords.add("down");
        self.stopWords.add("downwards");
        self.stopWords.add("during");
        self.stopWords.add("e");
        self.stopWords.add("each");
        self.stopWords.add("edu");
        self.stopWords.add("eg");
        self.stopWords.add("eight");
        self.stopWords.add("either");
        self.stopWords.add("else");
        self.stopWords.add("elsewhere");
        self.stopWords.add("empty");
        self.stopWords.add("enough");
        self.stopWords.add("entirely");
        self.stopWords.add("especially");
        self.stopWords.add("et");
        self.stopWords.add("etc");
        self.stopWords.add("even");
        self.stopWords.add("ever");
        self.stopWords.add("every");
        self.stopWords.add("everybody");
        self.stopWords.add("everyone");
        self.stopWords.add("everything");
        self.stopWords.add("everywhere");
        self.stopWords.add("ex");
        self.stopWords.add("exactly");
        self.stopWords.add("except");
        self.stopWords.add("f");
        self.stopWords.add("far");
        self.stopWords.add("few");
        self.stopWords.add("fifth");
        self.stopWords.add("first");
        self.stopWords.add("five");
        self.stopWords.add("for");
        self.stopWords.add("former");
        self.stopWords.add("formerly");
        self.stopWords.add("forth");
        self.stopWords.add("forty");
        self.stopWords.add("four");
        self.stopWords.add("from");
        self.stopWords.add("front");
        self.stopWords.add("full");
        self.stopWords.add("further");
        self.stopWords.add("furthermore");
        self.stopWords.add("g");
        self.stopWords.add("get");
        self.stopWords.add("gets");
        self.stopWords.add("getting");
        self.stopWords.add("given");
        self.stopWords.add("gives");
        self.stopWords.add("go");
        self.stopWords.add("goes");
        self.stopWords.add("going");
        self.stopWords.add("gone");
        self.stopWords.add("got");
        self.stopWords.add("gotten");
        self.stopWords.add("greetings");
        self.stopWords.add("gs");
        self.stopWords.add("h");
        self.stopWords.add("had");
        self.stopWords.add("hadn");
        self.stopWords.add("happens");
        self.stopWords.add("hardly");
        self.stopWords.add("has");
        self.stopWords.add("hasn");
        self.stopWords.add("hasnt");
        self.stopWords.add("have");
        self.stopWords.add("haven");
        self.stopWords.add("having");
        self.stopWords.add("he");
        self.stopWords.add("hello");
        self.stopWords.add("help");
        self.stopWords.add("hence");
        self.stopWords.add("her");
        self.stopWords.add("here");
        self.stopWords.add("hereafter");
        self.stopWords.add("hereby");
        self.stopWords.add("herein");
        self.stopWords.add("hereupon");
        self.stopWords.add("hers");
        self.stopWords.add("herself");
        self.stopWords.add("hi");
        self.stopWords.add("him");
        self.stopWords.add("himself");
        self.stopWords.add("his");
        self.stopWords.add("hither");
        self.stopWords.add("hopefully");
        self.stopWords.add("how");
        self.stopWords.add("howbeit");
        self.stopWords.add("however");
        self.stopWords.add("hundred");
        self.stopWords.add("i");
        self.stopWords.add("ie");
        self.stopWords.add("if");
        self.stopWords.add("ignored");
        self.stopWords.add("immediate");
        self.stopWords.add("in");
        self.stopWords.add("inasmuch");
        self.stopWords.add("inc");
        self.stopWords.add("inc.");
        self.stopWords.add("indeed");
        self.stopWords.add("inner");
        self.stopWords.add("insofar");
        self.stopWords.add("instead");
        self.stopWords.add("interest");
        self.stopWords.add("into");
        self.stopWords.add("inward");
        self.stopWords.add("is");
        self.stopWords.add("it");
        self.stopWords.add("its");
        self.stopWords.add("itself");
        self.stopWords.add("j");
        self.stopWords.add("just");
        self.stopWords.add("k");
        self.stopWords.add("keep");
        self.stopWords.add("keeps");
        self.stopWords.add("kept");
        self.stopWords.add("know");
        self.stopWords.add("known");
        self.stopWords.add("knows");
        self.stopWords.add("l");
        self.stopWords.add("last");
        self.stopWords.add("lately");
        self.stopWords.add("later");
        self.stopWords.add("latter");
        self.stopWords.add("latterly");
        self.stopWords.add("least");
        self.stopWords.add("less");
        self.stopWords.add("lest");
        self.stopWords.add("let");
        self.stopWords.add("like");
        self.stopWords.add("liked");
        self.stopWords.add("likely");
        self.stopWords.add("little");
        self.stopWords.add("look");
        self.stopWords.add("looking");
        self.stopWords.add("looks");
        self.stopWords.add("ltd");
        self.stopWords.add("m");
        self.stopWords.add("made");
        self.stopWords.add("mainly");
        self.stopWords.add("make");
        self.stopWords.add("makes");
        self.stopWords.add("many");
        self.stopWords.add("may");
        self.stopWords.add("maybe");
        self.stopWords.add("me");
        self.stopWords.add("mean");
        self.stopWords.add("meantime");
        self.stopWords.add("meanwhile");
        self.stopWords.add("merely");
        self.stopWords.add("might");
        self.stopWords.add("mine");
        self.stopWords.add("miss");
        self.stopWords.add("more");
        self.stopWords.add("moreover");
        self.stopWords.add("most");
        self.stopWords.add("mostly");
        self.stopWords.add("move");
        self.stopWords.add("mr");
        self.stopWords.add("mrs");
        self.stopWords.add("much");
        self.stopWords.add("must");
        self.stopWords.add("my");
        self.stopWords.add("myself");
        self.stopWords.add("n");
        self.stopWords.add("name");
        self.stopWords.add("namely");
        self.stopWords.add("nd");
        self.stopWords.add("near");
        self.stopWords.add("nearly");
        self.stopWords.add("necessary");
        self.stopWords.add("need");
        self.stopWords.add("needs");
        self.stopWords.add("neither");
        self.stopWords.add("never");
        self.stopWords.add("nevertheless");
        self.stopWords.add("new");
        self.stopWords.add("next");
        self.stopWords.add("nine");
        self.stopWords.add("no");
        self.stopWords.add("nobody");
        self.stopWords.add("non");
        self.stopWords.add("none");
        self.stopWords.add("nonetheless");
        self.stopWords.add("noone");
        self.stopWords.add("nor");
        self.stopWords.add("normally");
        self.stopWords.add("not");
        self.stopWords.add("nothing");
        self.stopWords.add("novel");
        self.stopWords.add("now");
        self.stopWords.add("nowhere");
        self.stopWords.add("o");
        self.stopWords.add("obviously");
        self.stopWords.add("of");
        self.stopWords.add("off");
        self.stopWords.add("often");
        self.stopWords.add("oh");
        self.stopWords.add("ok");
        self.stopWords.add("okay");
        self.stopWords.add("old");
        self.stopWords.add("on");
        self.stopWords.add("once");
        self.stopWords.add("one");
        self.stopWords.add("ones");
        self.stopWords.add("only");
        self.stopWords.add("onto");
        self.stopWords.add("or");
        self.stopWords.add("other");
        self.stopWords.add("others");
        self.stopWords.add("otherwise");
        self.stopWords.add("ought");
        self.stopWords.add("our");
        self.stopWords.add("ours");
        self.stopWords.add("ourselves");
        self.stopWords.add("out");
        self.stopWords.add("outside");
        self.stopWords.add("over");
        self.stopWords.add("overall");
        self.stopWords.add("own");
        self.stopWords.add("p");
        self.stopWords.add("part");
        self.stopWords.add("particular");
        self.stopWords.add("particularly");
        self.stopWords.add("per");
        self.stopWords.add("perhaps");
        self.stopWords.add("please");
        self.stopWords.add("plus");
        self.stopWords.add("possible");
        self.stopWords.add("presumably");
        self.stopWords.add("probably");
        self.stopWords.add("provides");
        self.stopWords.add("put");
        self.stopWords.add("q");
        self.stopWords.add("que");
        self.stopWords.add("quite");
        self.stopWords.add("qv");
        self.stopWords.add("r");
        self.stopWords.add("rather");
        self.stopWords.add("rd");
        self.stopWords.add("re");
        self.stopWords.add("really");
        self.stopWords.add("reasonably");
        self.stopWords.add("recent");
        self.stopWords.add("recently");
        self.stopWords.add("regarding");
        self.stopWords.add("regardless");
        self.stopWords.add("regards");
        self.stopWords.add("relatively");
        self.stopWords.add("respectively");
        self.stopWords.add("right");
        self.stopWords.add("s");
        self.stopWords.add("said");
        self.stopWords.add("same");
        self.stopWords.add("saw");
        self.stopWords.add("say");
        self.stopWords.add("saying");
        self.stopWords.add("says");
        self.stopWords.add("second");
        self.stopWords.add("secondly");
        self.stopWords.add("see");
        self.stopWords.add("seeing");
        self.stopWords.add("seem");
        self.stopWords.add("seemed");
        self.stopWords.add("seeming");
        self.stopWords.add("seems");
        self.stopWords.add("seen");
        self.stopWords.add("self");
        self.stopWords.add("selves");
        self.stopWords.add("sensible");
        self.stopWords.add("sent");
        self.stopWords.add("serious");
        self.stopWords.add("seriously");
        self.stopWords.add("seven");
        self.stopWords.add("several");
        self.stopWords.add("shall");
        self.stopWords.add("she");
        self.stopWords.add("should");
        self.stopWords.add("shouldn");
        self.stopWords.add("show");
        self.stopWords.add("side");
        self.stopWords.add("since");
        self.stopWords.add("sincere");
        self.stopWords.add("six");
        self.stopWords.add("so");
        self.stopWords.add("some");
        self.stopWords.add("somebody");
        self.stopWords.add("somehow");
        self.stopWords.add("someone");
        self.stopWords.add("something");
        self.stopWords.add("sometime");
        self.stopWords.add("sometimes");
        self.stopWords.add("somewhat");
        self.stopWords.add("somewhere");
        self.stopWords.add("soon");
        self.stopWords.add("sorry");
        self.stopWords.add("still");
        self.stopWords.add("stop");
        self.stopWords.add("sub");
        self.stopWords.add("such");
        self.stopWords.add("sup");
        self.stopWords.add("sure");
        self.stopWords.add("system");
        self.stopWords.add("t");
        self.stopWords.add("take");
        self.stopWords.add("taken");
        self.stopWords.add("taking");
        self.stopWords.add("tell");
        self.stopWords.add("tends");
        self.stopWords.add("th");
        self.stopWords.add("than");
        self.stopWords.add("thank");
        self.stopWords.add("thanks");
        self.stopWords.add("thanx");
        self.stopWords.add("that");
        self.stopWords.add("thats");
        self.stopWords.add("the");
        self.stopWords.add("their");
        self.stopWords.add("theirs");
        self.stopWords.add("them");
        self.stopWords.add("themselves");
        self.stopWords.add("then");
        self.stopWords.add("thencethere");
        self.stopWords.add("there");
        self.stopWords.add("thereafter");
        self.stopWords.add("thereby");
        self.stopWords.add("therefore");
        self.stopWords.add("therein");
        self.stopWords.add("theres");
        self.stopWords.add("thereupon");
        self.stopWords.add("these");
        self.stopWords.add("they");
        self.stopWords.add("thick");
        self.stopWords.add("thin");
        self.stopWords.add("think");
        self.stopWords.add("third");
        self.stopWords.add("thirty");
        self.stopWords.add("this");
        self.stopWords.add("thorough");
        self.stopWords.add("thoroughly");
        self.stopWords.add("those");
        self.stopWords.add("though");
        self.stopWords.add("three");
        self.stopWords.add("through");
        self.stopWords.add("throughout");
        self.stopWords.add("thru");
        self.stopWords.add("thus");
        self.stopWords.add("to");
        self.stopWords.add("together");
        self.stopWords.add("too");
        self.stopWords.add("took");
        self.stopWords.add("top");
        self.stopWords.add("toward");
        self.stopWords.add("towards");
        self.stopWords.add("tried");
        self.stopWords.add("tries");
        self.stopWords.add("truly");
        self.stopWords.add("try");
        self.stopWords.add("trying");
        self.stopWords.add("twenty");
        self.stopWords.add("twice");
        self.stopWords.add("two");
        self.stopWords.add("u");
        self.stopWords.add("un");
        self.stopWords.add("under");
        self.stopWords.add("unfortunately");
        self.stopWords.add("unless");
        self.stopWords.add("unlike");
        self.stopWords.add("unlikely");
        self.stopWords.add("until");
        self.stopWords.add("unto");
        self.stopWords.add("up");
        self.stopWords.add("upon");
        self.stopWords.add("us");
        self.stopWords.add("use");
        self.stopWords.add("used");
        self.stopWords.add("useful");
        self.stopWords.add("uses");
        self.stopWords.add("using");
        self.stopWords.add("usually");
        self.stopWords.add("uucp");
        self.stopWords.add("v");
        self.stopWords.add("value");
        self.stopWords.add("various");
        self.stopWords.add("very");
        self.stopWords.add("vfor");
        self.stopWords.add("via");
        self.stopWords.add("viz");
        self.stopWords.add("vs");
        self.stopWords.add("w");
        self.stopWords.add("wait");
        self.stopWords.add("want");
        self.stopWords.add("wants");
        self.stopWords.add("was");
        self.stopWords.add("wasn");
        self.stopWords.add("way");
        self.stopWords.add("we");
        self.stopWords.add("welcome");
        self.stopWords.add("well");
        self.stopWords.add("wentwere");
        self.stopWords.add("weren");
        self.stopWords.add("what");
        self.stopWords.add("whatever");
        self.stopWords.add("when");
        self.stopWords.add("whence");
        self.stopWords.add("whenever");
        self.stopWords.add("where");
        self.stopWords.add("whereafter");
        self.stopWords.add("whereas");
        self.stopWords.add("whereby");
        self.stopWords.add("wherein");
        self.stopWords.add("whereupon");
        self.stopWords.add("wherever");
        self.stopWords.add("whether");
        self.stopWords.add("which");
        self.stopWords.add("while");
        self.stopWords.add("whither");
        self.stopWords.add("who");
        self.stopWords.add("whoever");
        self.stopWords.add("whole");
        self.stopWords.add("whom");
        self.stopWords.add("whomever");
        self.stopWords.add("whose");
        self.stopWords.add("why");
        self.stopWords.add("will");
        self.stopWords.add("willing");
        self.stopWords.add("wish");
        self.stopWords.add("with");
        self.stopWords.add("within");
        self.stopWords.add("without");
        self.stopWords.add("won");
        self.stopWords.add("wonder");
        self.stopWords.add("would");
        self.stopWords.add("wouldn");
        self.stopWords.add("x");
        self.stopWords.add("y");
        self.stopWords.add("yes");
        self.stopWords.add("yet");
        self.stopWords.add("you");
        self.stopWords.add("your");
        self.stopWords.add("yours");
        self.stopWords.add("yourself");
        self.stopWords.add("yourselves");
        self.stopWords.add("z");
        self.stopWords.add("zero");
        self.stopWords.add("people");
        self.stopWords.add("tagnum");
        self.stopWords.add("t1");
        self.stopWords.add("t2");
        self.stopWords.add("t3");
        self.stopWords.add("t4");
        self.stopWords.add("h1");
        self.stopWords.add("h2");
        self.stopWords.add("h3");
        self.stopWords.add("h4");
        self.stopWords.add("amp");
        self.stopWords.add("lt");
        self.stopWords.add("gt");
        self.stopWords.add("section");
        self.stopWords.add("cx");
   

