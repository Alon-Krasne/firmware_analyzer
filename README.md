# Firmware analyzer

### Comparision of processing time between different strategies

* **Synchronized run**: Going over the entire list of files one by one
* **Multiprocessing run**: Going over the entire list of files in parallel using multiprocessing

_Note: During investigation of the preferred method, `multithreading` and `async` were slower than Synchronized run so 
I'm not showing them in the comparison_

| Number of files | Synchronized time (seconds)   | Multiprocessing time (seconds) |
|-----------------|----------------------------|--------------------------------|
| 100             | 0.6112                     | 0.7928                         |
| 700             | 3.6074                     | 0.6225                         |
| 1800            | 9.8405                     | 0.8198                         |
| 3400            | 9.4722                     | 1.2460                         |
| 5500            | 14.3343                    | 1.0801                         |

Notice that for a small amount of files, the multiprocessing strategy is slower than the sync one. This is because 
the overhead of creating processes is higher than the time it takes to process the files. However, for a large amount 
of files, the multiprocessing strategy is faster than the sync one.