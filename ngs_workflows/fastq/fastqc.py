#!/usr/bin/env python

#    This file is part of ngs_workflow.
#
#    ngs_workflow is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ngs_workflow is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ngs_workflow.  If not, see <http://www.gnu.org/licenses/>.

import rpy2.robjects as robjects
from   rpy2.robjects.packages import importr
import fastq_info

def fastq_adjust(filename,filename_out=None,Ns=3,base_treshold=20):
   '''
   Reads the fastq file and adjust the reads quality
   '''
   shortread = importr('ShortRead')
   reads     = shortread.readFastq(filename)
   reads     = fastq_base_filter(reads,Ns=Ns,base_treshold=base_treshold)
   if filename_out:
      shortread.writeFastq(reads,filename_out)
   else:
      return reads

def fastq_base_filter(reads,Ns=3,base_treshold=20):
   '''
   It uses the ShortRead Bioconductr package and the
   rpy2 interface to filter the reads based on the nucleotides
   composition
   '''
   # Would be nice to do it like this:
   #filter1   = shortread.nFilter(threshold=Ns)
   #filter2   = shortread.polynFilter(threshold=base_treshold, nuc=robjects.vectors.StrVector("ACTG"))
   #filterall = shortread.compose(filter1,filter2)
   #idx_filt  = filterall(shortread.sread(reads))
   #reads     = reads.rx[idx_filt] ???? but the subscription does not works
   #Instead I would do like this.. for now:
   robjects.r('''
      basefilt <- function(reads, Ns, basetreshold) {
         require(ShortRead)
         filter1   <- nFilter(threshold=Ns)
         filter2   <- polynFilter(threshold=basetreshold, nuc=c("A","C","T","G"))
         filterall <- compose(filter1,filter2)
         reads[filterall(sread(reads))]
      }
   ''')
   return robjects.r['basefilt'](reads,Ns,base_treshold)

def fastq_adapters_quality_trim(filename,filename_out,adapter,min_length=15,min_qual=20,five_trim=5):
   '''
   Remove the provided adapter from a reads in the given fastq file
   also trim the 5prime to a certain base, and the 3prime by quality.
   finally keep only the reads with a cerain lenght after filtering
   '''
   shortread = importr('ShortRead')
   reads     = shortread.readFastq(filename)   
   robjects.r('''
      adap.quality.filt <- function(reads, adapter, min.length, min.qual,fivep.trim) {
         require(ShortRead)
         seqs <- sread(reads)
         mismatchVector <- c(rep(2,length(DNAString(adapter))))
         trimCoords <- trimLRPatterns(Rpattern=adapter, subject=seqs, max.Rmismatch=mismatchVector, ranges=T)
         letter_subject <- DNAString(paste(rep.int("N", width(seqs)[1]), collapse=""))
         subseq(seqs,start=end(trimCoords)+1,width=width(reads)-width(trimCoords)) <- letter <- as(Views(letter_subject, start=1, end=as.vector(width(reads)-width(trimCoords))), "DNAStringSet") 
         seqs <- DNAStringSet(seqs, start=fivep.trim)
         qual <- BStringSet(quality(quality(reads)), start=fivep.trim)
         qual <- PhredQuality(qual)
         myqual_mat <- matrix(charToRaw(as.character(unlist(qual))), nrow=length(qual), byrow=TRUE)
         at <- myqual_mat < charToRaw(as.character(PhredQuality(as.integer(min.qual))))
         letter <- as(Views(letter_subject, start=1, end=rowSums(at)), "DNAStringSet")
         injectedseqs <- replaceLetterAt(seqs, at, letter)
         nadapter <- paste(rep("N", max(width(injectedseqs))), sep="", collapse="")
         mismatchVector <- c(rep(0,width(nadapter)))
         trimCoords <- trimLRPatterns(Rpattern=nadapter, subject=injectedseqs, max.Rmismatch=mismatchVector, ranges=T)
         seqs <- DNAStringSet(seqs, start=start(trimCoords), end=end(trimCoords))
         qual <- BStringSet(qual, start=start(trimCoords), end=end(trimCoords))
         qual <- SFastqQuality(qual)
         trimmed <- ShortReadQ(sread=seqs, quality=qual, id=id(reads))
         trimmed <- trimmed[min.length <= width(sread(trimmed))]
         filter1   <- nFilter(threshold=0)
         filter2   <- polynFilter(threshold=round(max(width(trimmed))/3,0), nuc=c("A","C","T","G"))
         filterall <- compose(filter1,filter2)
         trimmed[filterall(sread(trimmed))]
         }
   ''')   
   if filename_out:
      shortread.writeFastq(robjects.r['adap.quality.filt'](reads,adapter,min_length,min_qual,five_trim)
   else:
      return robjects.r['adap.quality.filt'](reads,adapter,min_length,min_qual,five_trim)
      
      
def find_adapter(reads,fasta):
   '''
   Given a fastq and a fasta files containig the more common adapters used
   this function will give the adapters that whas probably used.
   '''
   pass
   
def fastqc_report_grab_overappresented(fastqc_data):
   '''
   From the FastQC report (from FasqQC tool in java) grab the over rapresented
   sequences line
   '''
   over_seqs = []
   with open(fastqc_data, 'rb') as fastqc:
      semaphore = 'red'
      for line in fastqc:
         if semaphore == 'red':
            pass
         elif semaphore == 'green':
            if line.startswith('>>END_MODULE'):
               break
            elif line.startswith('#'):
               pass
            else:
               over_seqs.append(str(line.strip()))
         if line.startswith('>>Overrepresented sequences'):
            semaphore = 'green'
      return over_seqs